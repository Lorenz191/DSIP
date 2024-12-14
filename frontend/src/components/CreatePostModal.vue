<script setup>
import axios from 'axios'
import { ref, defineEmits } from 'vue'

// Inputs for the new post's title and content
const newPostTitle = ref("")
const newPostContent = ref("")
const isAnonym = ref(false)

// Emit event to close the modal
const emit = defineEmits(['close'])

// Close the modal and clear inputs
function closeCreatePostModal() {
  emit('close') // Notify parent to close the modal
  newPostTitle.value = ""
  newPostContent.value = ""
  isAnonym.value = false
}


// Create a new post and add it to the list
const createPost = async () => {
  try {
    // Send POST request to API with new post data
    await axios.post('http://localhost:8000/api/post/create/', {
      "body": {"title": newPostTitle.value,
                "content": newPostContent.value},
      "is_anonym": isAnonym.value
    })
    // Close the modal after saving
    closeCreatePostModal()
  } catch (error) {
    console.error('Error creating post:', error)
  }
}
</script>

<template>
<div class="modal">
      <h2>Neuer Beitrag</h2>
      <form @submit.prevent="createPost">
        <!-- Input for the post title -->
        <div class="form-group">
          <label for="title">Titel</label>
          <input
            id="title"
            v-model="newPostTitle"
            type="text"
            placeholder="Titel eingeben"
            required
          />
        </div>
        <!-- Textarea for the post content -->
        <div class="form-group">
          <label for="content">Text</label>
          <textarea
            id="content"
            v-model="newPostContent"
            placeholder="Text eingeben"
            rows="5"
            required
          ></textarea>
        </div>
        <!-- Buttons to cancel or save the post -->
        <div class="modal-buttons">
          <button type="button" @click="closeCreatePostModal" class="cancel-button">
            Abbrechen
          </button>
          <button type="submit" class="save-button">
            Speichern
          </button>
        </div>
      </form>
    </div>
</template>

<style scoped>

.modal {
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
  width: 400px;
  text-align: center;
}

.form-group {
  margin-bottom: 15px;
  text-align: left;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

input,
textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 14px;
}

.modal-buttons {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  margin-top: 20px;
}

.cancel-button,
.save-button {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  font-size: 14px;
  cursor: pointer;
}

.cancel-button {
  background: #ccc;
  color: black;
}

.save-button {
  background: #4caf50;
  color: white;
}
</style>
