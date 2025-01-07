<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <div class="warning-container">
        <span>&#9888; Willst du diesen Post wirklich löschen?</span>
      </div>
      <div class="modal-actions">
        <button @click="$emit('confirm')">Ja</button>
        <button @click="$emit('cancel')">Nein</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DeletionModal'
}
</script>

<style scoped>
* {
  font-family: 'Futura';
}

.modal-overlay {
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

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
}

.modal-actions {
  margin-top: 20px;
  display: flex;
  justify-content: space-around;
}

button {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #2edb7b;
}

span {
  display: inline-block;
  width: auto;
  color: orange;
  font-size: 1em;
  font-weight: bold;
  border-radius: 20%;
}

.warning-container {
  padding: 5px;
  margin-top: 1vh;
  background-color: rgba(255, 165, 0, 0.24);
  width: 100%;
  border-radius: 0.3vw;
  border: 2px solid orange;
}
</style>
