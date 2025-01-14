<script setup>
import { useSessionStore } from '@/stores/session.js'
import { ref } from 'vue'
import axios from 'axios'

const props = defineProps({
  comment: {
    type: Object,
    required: true
  }
})

const date = new Date(props.comment.created_at).toLocaleDateString()
const admin = ref(useSessionStore().isAdmin)
const emits = defineEmits(['delete'])


const deleteComment = async () => {
  try {
    emits('delete', {"_id": props.comment._id})
  } catch (error) {
    console.error('Error deleting comment:', error)
  }
}

</script>

<template>
  <div class="content-container">
    <div class="metadata-container">
      <p class="author">{{ comment.author }}</p>
      <div class="deletion-date-container">
        <button v-if="admin" @click="deleteComment">&#x1F5D1;</button>
        <p class="date">{{ date }}</p>
      </div>
    </div>
    <div class="data-container">
      <p class="comment-content">{{ comment.comment }}</p>
    </div>
  </div>
</template>

<style scoped>
p, h1 {
  font-family: Futura;
}

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

.deletion-date-container{
  display: flex;
  flex-direction: row;
  gap: 10px;
}
.deletion-date-container:hover{
  cursor: pointer;
}

.date{
  color: grey;
}

.data-container {
  padding: 10px 0;
}

.author{
  color: #2edb7b;
}
</style>
