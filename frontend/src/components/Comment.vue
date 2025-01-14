<script setup>
const props = defineProps({
  comment: {
    type: Object,
    required: true
  }
})

const date = new Date(props.comment.created_at).toLocaleDateString()
</script>

<template>
  <div class="content-container">
    <div class="metadata-container">
      <p>{{ comment.author }}</p>
      <p>{{ date }}</p>
    </div>
    <div class="data-container">
      <p class="comment-content">{{ comment.comment }}</p>
    </div>
  </div>
</template>

<style scoped>
.content-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
  border: 1px grey solid;
  border-radius: 10px;
  padding: 10px;
}

.metadata-container{
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}
</style>
