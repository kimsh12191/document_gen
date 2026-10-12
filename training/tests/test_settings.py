import contextlib
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

import train
from bank_ocr.settings import load_settings
from bank_ocr.cli import main as cli_main
from benchmark_report import build_report


class SettingsTests(unittest.TestCase):
    def test_comparison_rejects_different_additional_generation_settings(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            base = {'tasks_sha256': 'same', 'model_label': 'Base',
                    'reference_type': 'ocr_pseudo_unreviewed',
                    'tasks': {'crop_ocr': {'count': 1, 'cer': 0, 'em': 1}},
                    'inference': {'temperature': 0, 'max_tokens': 256, 'enable_thinking': False}}
            one, two = root / 'one.json', root / 'two.json'
            one.write_text(json.dumps(base))
            base['model_label'] = 'SFT'
            base['inference']['request_options'] = {'top_p': 0.9}
            two.write_text(json.dumps(base))
            with self.assertRaisesRegex(ValueError, 'request_options'):
                build_report([one, two], root / 'comparison.csv')
            args = ['bank-ocr', 'compare', str(one), str(two), '--out', str(root / 'comparison.csv')]
            with patch.object(sys, 'argv', args), self.assertRaisesRegex(ValueError, 'request_options'):
                cli_main()
            base['inference']['request_options'] = {}
            two.write_text(json.dumps(base))
            build_report([one, two], root / 'comparison.csv')
            self.assertTrue((root / 'comparison.html').is_file())

    def test_training_config_and_gpu_environment_reach_subprocess(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            model = root / 'model'
            data = root / 'data'
            out = root / 'run'
            model.mkdir()
            data.mkdir()
            (data / 'DONE.json').write_text('{}')
            (data / 'train_sft.jsonl').write_text('{"id":"train"}\n')
            cfg = root / 'train.json'
            cfg.write_text(json.dumps({'learning_rate': 0.0002, 'lora_rank': 32,
                                       'target_modules': ['q_proj', 'v_proj'],
                                       'gradient_checkpointing_kwargs': {'use_reentrant': False}, 'max_steps': 100}))
            args = ['train.py', 'sft', '--config', str(cfg), '--model', str(model),
                    '--data', str(data), '--output', str(out), '--max-steps', '5', '--execute']
            with patch.object(sys, 'argv', args), patch.dict(os.environ, {'CUDA_VISIBLE_DEVICES': '4,5,6,7'}), \
                    patch('train.importlib.metadata.version', return_value='4.0.4'), \
                    patch('train.importlib.metadata.distributions', return_value=[]), \
                    patch('train.subprocess.run') as run, contextlib.redirect_stdout(io.StringIO()):
                train.main()
            command = run.call_args.args[0]
            env = run.call_args.kwargs['env']
            self.assertEqual(env['CUDA_VISIBLE_DEVICES'], '4,5,6,7')
            self.assertEqual(env['NPROC_PER_NODE'], '4')
            self.assertEqual(command[command.index('--learning_rate') + 1], '0.0002')
            self.assertEqual(command[command.index('--max_steps') + 1], '5')
            self.assertEqual(command[command.index('--model_type') + 1], 'qwen3_5')
            self.assertEqual(command[command.index('--target_modules') + 1:command.index('--target_modules') + 3], ['q_proj', 'v_proj'])
            resolved = load_settings(out / 'training.resolved.json')
            self.assertEqual(resolved['lora_rank'], 32)
            self.assertEqual(resolved['model_type'], 'qwen3_5')
            self.assertEqual(load_settings(out / 'launch.json')['cuda_visible_devices'], '4,5,6,7')
            with patch.object(sys, 'argv', args + ['--gpus', '0,2']), \
                    patch.dict(os.environ, {'CUDA_VISIBLE_DEVICES': '4,5,6,7'}), \
                    patch('train.importlib.metadata.version', return_value='4.0.4'), \
                    patch('train.importlib.metadata.distributions', return_value=[]), \
                    patch('train.subprocess.run') as run, contextlib.redirect_stdout(io.StringIO()):
                train.main()
            self.assertEqual(run.call_args.kwargs['env']['CUDA_VISIBLE_DEVICES'], '0,2')
            self.assertEqual(run.call_args.kwargs['env']['NPROC_PER_NODE'], '2')
            cfg.write_text(json.dumps({'model_type': 'configured_type'}))
            for flag, expected in [(None, 'configured_type'), ('--model-type', 'qwen3_5'),
                                   ('--model_type', 'qwen3_5')]:
                override = [flag, 'qwen3_5'] if flag else []
                with self.subTest(flag=flag), patch.object(sys, 'argv', args + override), \
                        patch('train.importlib.metadata.version', return_value='4.0.4'), \
                        patch('train.importlib.metadata.distributions', return_value=[]), \
                        patch('train.subprocess.run') as run, contextlib.redirect_stdout(io.StringIO()):
                    train.main()
                command = run.call_args.args[0]
                self.assertEqual(command[command.index('--model_type') + 1], expected)

    def test_invalid_gpu_selections(self):
        for ids in ['', '0,0', '-1', '0,', 'all']:
            with self.assertRaises(ValueError):
                train.gpu_selection(ids)

    def test_inference_config_cli_override(self):
        with tempfile.TemporaryDirectory() as temp:
            cfg = Path(temp) / 'inference.json'
            cfg.write_text(json.dumps({'temperature': 0.4, 'max_tokens': 512,
                                       'enable_thinking': True, 'request_options': {'top_p': 0.9}}))
            args = ['bank-ocr', 'predict', '--tasks', 'tasks', '--out', 'out', '--run-id', 'sft-2',
                    '--config', str(cfg), '--max-tokens', '128', '--no-enable-thinking']
            with patch.object(sys, 'argv', args), patch('bank_ocr.cli.predict', return_value={}) as predict, \
                    contextlib.redirect_stdout(io.StringIO()):
                cli_main()
            self.assertEqual(predict.call_args.kwargs['max_tokens'], 128)
            self.assertEqual(predict.call_args.kwargs['temperature'], 0.4)
            self.assertFalse(predict.call_args.kwargs['enable_thinking'])
            self.assertEqual(predict.call_args.kwargs['request_options'], {'top_p': 0.9})


if __name__ == '__main__':
    unittest.main()
