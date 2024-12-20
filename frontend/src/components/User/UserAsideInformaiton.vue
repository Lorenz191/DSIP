<script setup>

const props = defineProps({
  svPosts: {
    type: Boolean,
    required: true
  }
})

const emit = defineEmits(['update:svPosts'])

const toggleSvPosts = () => {
  emit('update:svPosts', !props.svPosts)
}
</script>

<template>
  <div class="aside-container">
    <div
      class="top-container"
      :class="{ 'clicked': props.svPosts }"
      @click="toggleSvPosts"
    >
      <img src="../icons/Chat_Bubbles.svg" alt="Chat Bubbles" class="chat-icon">
    </div>
    <div class="seperation-container">
      <svg xmlns="http://www.w3.org/2000/svg" width="100px" height="5" viewBox="0 0 69 5" fill="none" id="line">
        <path d="M2.7037 2.80457H66.2963"  stroke="#6FD1DE" stroke-opacity="0.85" stroke-width="4" stroke-linecap="round" />
        <path d="M2.7037 2.80457H66.2963"  stroke="#2EDB7B" stroke-opacity="0.85" stroke-width="4" stroke-linecap="round" v-if="props.svPosts"/>
      </svg>
    </div>
    <div
      class="bottom-container"
      :class="{ 'clicked': props.svPosts }"
      @click="toggleSvPosts"
    >
      <img src="../icons/Megaphone.svg" alt="Megaphone" class="megaphone">
    </div>
  </div>
</template>


<style scoped>
.aside-container {
  width: 100px;
  height: 240px;
}

.top-container, .bottom-container {
  width: 100px;
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

.bottom-container, .top-container {
  display: flex;
  justify-content: center;
  align-items: center;
}

.megaphone, .chat-icon {
  width: 60px;
}

.bottom-container:hover, .top-container:hover {
  cursor: pointer;
}

.bottom-container.clicked {
  border-bottom: 5px solid #2EDB7B;
  border-right: 5px solid #2EDB7B;
  border-left: 5px solid #2EDB7B;
}

.top-container.clicked {
  border-top: 2px solid rgba(221, 221, 221, 0.87);
  border-right: 2px solid rgba(221, 221, 221, 0.87);
  border-left: 2px solid rgba(221, 221, 221, 0.87);
}

</style>
