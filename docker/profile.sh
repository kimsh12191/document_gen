# SSH 로 들어왔을 때 바로 docgen 을 쓸 수 있게
export PATH=/opt/venv/bin:$PATH LANG=C.UTF-8 PLAYWRIGHT_BROWSERS_PATH=/opt/ms-playwright PYTHONPATH=/home/docgen/document_gen PYTHONUNBUFFERED=1
if [ -n "$PS1" ] && [ "$PWD" = "$HOME" ]; then
    cd "$HOME/document_gen"
    echo "docgen: python -m docgen --help | 벤치마크: python -m docgen.bench --help | 결과 저장: /out"
fi
