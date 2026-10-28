"use strict";

addRoute(/^#\/ocr-examples(?:\/(\w+))?$/, task => viewOcrExamples(task), "ocr-examples");

async function viewOcrExamples(task) {
  const data = await api("/api/ocr-examples");
  const item = data.examples.find(x => x.task === task) || data.examples[0];
  const pretty = value => JSON.stringify(value, null, 2);
  main().innerHTML = `<h1>OCR 예시</h1>
    <p class="sub">데이터셋을 생성하기 전에 과제별 입력 이미지·질문·정답을 확인하세요. 과제를 선택하면 같은 가이드 예시가 표시됩니다.</p>
    <div class="bar"><a href="#/guide/studio.md">합성 OCR 만들기</a><a href="#/guide/ocr.md">내 이미지로 OCR 데이터</a><a href="#/datasets">생성·등록한 데이터셋의 문항 보기</a></div>
    <div class="ocr-task-grid">${data.examples.map(x => `<a href="#/ocr-examples/${esc(x.task)}" class="panel ${item.task === x.task ? 'ocr-task-selected' : ''}" ${item.task === x.task ? 'aria-current="page"' : ''}><b>${esc(x.title)}</b><br><span class="mono muted">${esc(x.task)}</span></a>`).join("")}</div>
    <h2>${esc(item.title)} <span class="mono muted">${esc(item.task)}</span></h2>
    <p>${esc(item.how)}</p><p class="sub">${esc(data.note)}</p>
    <div class="ocr-example-layout">
      <section class="panel"><h3>모델에 주는 입력 이미지</h3><p class="sub">이미지를 누르면 크게 볼 수 있습니다.</p>
        <a href="${esc(item.input_image)}" target="_blank" rel="noopener"><img class="ocr-example-image" src="${esc(item.input_image)}" alt="${esc(item.title)} 입력 이미지"></a>
        ${item.annotated_images.length ? `<details id="ocr-annotation"><summary>정답 위치·질문 영역 표시 보기 (설명용)</summary><p class="sub">초록: 정답 박스 · 파랑: 질문에 준 영역. 이 표시는 모델 입력에 추가되지 않습니다. 색 박스 과제의 원래 입력 표시는 입력 이미지에 포함됩니다.</p>${item.annotated_images.map(url => `<a href="${esc(url)}" target="_blank" rel="noopener"><img class="ocr-example-image" src="${esc(url)}" alt="${esc(item.title)} 정답 위치 설명 이미지" loading="lazy"></a>`).join("")}</details>` : ""}
      </section>
      <section><div class="panel"><h3>질문</h3><pre class="ans mono">${esc(item.prompt)}</pre></div>
        <div class="panel"><h3>모델이 출력해야 하는 답</h3><pre class="ans mono" id="ocr-model-answer">${esc(item.model_answer)}</pre></div>
        <div class="panel"><h3>채점 기준</h3><p>${esc(item.score)}</p></div>
        <details class="panel"><summary>데이터에 저장된 정답 target</summary><pre class="ans mono">${esc(pretty(item.target))}</pre></details>
        <details class="panel"><summary>원본 OCR 준비 문항 JSON</summary><p class="sub">경로의 &lt;prepared&gt;는 원래 생성 폴더를 뜻하는 예시 자리입니다. 현재 과제 폴더는 prompt·answer 형식으로도 제공됩니다.</p><pre class="ans mono">${esc(pretty(item.record))}</pre></details>
      </section>
    </div>`;
  main().scrollTop = 0;
}
