<script setup>
import { ref } from 'vue'

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  content: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['close', 'save'])

const editableTitle = ref(props.title)
const editableContent = ref(props.content)

const close = () => {
  emit('close')
}

const save = () => {
  emit('save', { title: editableTitle.value, content: editableContent.value })
}
</script>

<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <div class="header">
        <h1>Post bearbeiten:</h1>
        <button class="exit" @click="close">X</button>
      </div>
      <div class="title-container">
        <input placeholder="Titel" class="titel" v-model="editableTitle"/>
      </div>
      <div class="content-container">
        <textarea placeholder="Teile deinen Vorschlag mit uns..." class="textarea" v-model="editableContent"></textarea>
      </div>
      <div class="button-container">
        <button class="save" @click="save">Speichern</button>
      </div>
    </div>
  </div>
</template>

<style scoped>

.modal-overlay {
  font-family: Futura, sans-serif;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}
h1{
  font-weight: bold;
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  width: 320px;
}

.header{
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.titel {
  margin-top: 30px;
  text-indent: 10px;
  border: 1px grey solid;
  border-radius: 10px;
  width: 100%;
  height: 5vh;
}

.textarea {
  resize: none;
  text-indent: 10px;
  margin-top: 20px;
  border: 1px grey solid;
  border-radius: 10px;
  width: 100%;
  height: 20vh;
  min-height: 25vh;
  max-height: 600px;
  overflow: scroll;
}

.exit{
  color: grey;
}

.button-container{
  margin-top: 10px;
}

.save{
  padding: 7px;
  background: #2edb7b;
  color: white;
  border-radius: 5px;
  margin:5px;
}

.save:hover{
  background: #229f5a;
  cursor: pointer;
}

.close:hover{
  cursor: pointer;
}
</style>
