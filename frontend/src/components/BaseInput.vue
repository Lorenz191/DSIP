<script setup>

const props = defineProps({
  type: {
    type: String,
    required: true
  }
})


</script>

<template>
  <div class="input-container">
    <div class="input-label">
      <label :for="props.type"><slot>Label</slot></label>
    </div>
    <div class="input">
      <input :type="props.type" :id="props.type">
    </div>
  </div>
</template>

<style scoped>

</style>
