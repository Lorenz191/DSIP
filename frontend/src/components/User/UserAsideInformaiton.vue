<script setup>

</script>

<template>
  <div class="aside-container">
    <div class="top-container">

    </div>
    <div class="seperation-container">
      <svg xmlns="http://www.w3.org/2000/svg" width="100px" height="5" viewBox="0 0 69 5" fill="none">
        <path d="M2.7037 2.80457H66.2963" stroke="#6FD1DE" stroke-opacity="0.85" stroke-width="4" stroke-linecap="round"/>
      </svg>
    </div>
    <div class="bottom-container">

    </div>
  </div>
</template>

<style scoped>
.aside-container {
  width: 100px;
  height: 240px;
}

.top-container, .bottom-container {
  width: 100%;
  height: 120px;
}

.top-container {
  border-radius: 30px 30px 0px 0px;
  border-top: 5px solid rgba(111, 209, 222, 0.85);
  border-right: 5px solid rgba(111, 209, 222, 0.85);
  border-left: 5px solid rgba(111, 209, 222, 0.85);
  background: #FFF;
}

.bottom-container {
  border-radius: 0px 0px 30px 30px;
  border-bottom: 2px solid rgba(221, 221, 221, 0.87);
  border-right: 2px solid rgba(221, 221, 221, 0.87);
  border-left: 2px solid rgba(221, 221, 221, 0.87);
  background: #FFF;
}
</style>
