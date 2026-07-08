<template>
  <div class="boundground-hierarchy" aria-label="Boundground hierarchy">
    <div class="boundground-hierarchy__item boundground-hierarchy__item--outer">Outer Boundary</div>

    <div class="boundground-hierarchy__connector" aria-hidden="true"></div>

    <div class="boundground-hierarchy__item boundground-hierarchy__item--inner">Boundary</div>
  </div>
</template>

<style scoped>
.boundground-hierarchy {
  display: grid;
  width: 100%;
  height: 100%;
  grid-template-rows: minmax(0, 1fr) 0.8fr minmax(0, 1fr);
  place-items: center;
  padding: 8px 10px 10px;
}

.boundground-hierarchy__item {
  display: grid;
  width: 100%;
  height: 100%;
  min-height: 0;
  place-items: center;
  background: rgb(255 255 255 / 92%);
  color: #aaa;
  font-size: clamp(0.88rem, 8.4cqw, 1.35rem);
  font-weight: 900;
  letter-spacing: 0;
  line-height: 1;
  text-align: center;
  white-space: nowrap;
}

.boundground-hierarchy__item--outer {
  border: 2px dashed #1e1e1e;
}

.boundground-hierarchy__item--inner {
  border: 2px solid #1e1e1e;
}

.boundground-hierarchy__connector {
  width: 3px;
  height: 100%;
  background: #1e1e1e;
}
</style>
