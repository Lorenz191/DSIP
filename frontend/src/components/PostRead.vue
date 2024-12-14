<script setup>
import { ref } from 'vue'
import { RouterLink } from 'vue-router'

const props = defineProps({
  post: {
    type: Object,
    required: true
  }
})
const status = ref(props.post.status);

const date = new Date(props.post.created_at).toLocaleDateString()

const upvoted = ref(false)
const downvoted = ref(false)
const hover_up = ref(false)
const hover_down = ref(false)

const handleUpvote = () => {
  hover_down.value = false;
  if (!upvoted.value) {
    upvoted.value = true
    downvoted.value = false
  } else {
    upvoted.value = false
  }
}

const handleDownvote = () => {
  hover_up.value = false;
  if (!downvoted.value) {
    downvoted.value = true
    upvoted.value = false
  } else {
    downvoted.value = false
  }
}
</script>

<template>
  <div class="post-container">
    <RouterLink :to="`/post/${props.post._id}`">
      <div class="date-container">
        <p class="date">Veröffentlicht am {{ date }}</p>
        <p class="status">{{status}}</p>
      </div>
      <div class="title-container">
        <h1 class="title">{{ props.post.body.title }}</h1>
      </div>
      <div class="seperation-line-container">
        <svg xmlns="http://www.w3.org/2000/svg" width="720" height="4" viewBox="0 0 720 4" fill="none">
          <path d="M2 2H699.5" stroke="#333333" stroke-opacity="0.2" stroke-width="3" stroke-linecap="round" />
        </svg>
      </div>
      <div class="text-container">
        <p class="post-body">
          {{ props.post.body.content }}
        </p>
      </div>
    </RouterLink>
    <div class="seperation-line-container">
      <svg xmlns="http://www.w3.org/2000/svg" width="720" height="4" viewBox="0 0 720 4" fill="none">
        <path d="M2 2H699.5" stroke="#333333" stroke-opacity="0.2" stroke-width="3" stroke-linecap="round" />
      </svg>
    </div>
    <div class="voting-container-container">
      <div class="voting-container">
        <div class="upvote">
          <img src="./icons/Arrow_Up_Black.svg" alt="upvote" style="height: 36px;" v-if="!upvoted && !hover_up"
               @click="handleUpvote" @mouseover="hover_up = true" @mouseleave="hover_up = false">
          <img src="./icons/Arrow_Up_Green_Filled.svg" alt="upvote" style="height: 36px;" v-if="upvoted"
               @click="handleUpvote">
          <img src="./icons/Arrow_Up_Green.svg" alt="upvote" style="height: 36px;" v-if="hover_up && !upvoted"
               @click="handleUpvote" @mouseover="hover_up = true" @mouseleave="hover_up = false">
        </div>
        <div class="vertical-seperation-line">
          <svg xmlns="http://www.w3.org/2000/svg" width="2" height="36" viewBox="0 0 2 36" fill="none">
            <path d="M1 1V34.5" stroke="#D9D9D9" stroke-opacity="0.5" stroke-width="1.5" stroke-linecap="round" />
          </svg>
        </div>
        <div class="downvote">
          <img src="./icons/Arrow_Down_Blackl.svg" alt="downvote" style="height: 36px;" v-if="!downvoted && !hover_down"
               @click="handleDownvote" @mouseover="hover_down = true" @mouseleave="hover_down = false">
          <img src="./icons/Arrow_Down_Blue_Filled.svg" alt="downvote" style="height: 36px;" v-if="downvoted"
               @click="handleDownvote">
          <img src="./icons/Arrow_Down_Blue.svg" alt="downvote" style="height: 36px;" v-if="hover_down && !downvoted"
               @click="handleDownvote" @mouseover="hover_down = true" @mouseleave="hover_down = false">
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.post-container {
  margin-bottom: 60px;
  width: 800px;
  height: auto;
  padding-bottom: 10px;
  box-shadow: 5px 5px 15px 0px rgba(0, 0, 0, 0.25);
  border-radius: 20px;
  border: 3px solid rgba(217, 217, 217, 0.20);
  background: #FFF;
}

.date-container {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  padding: 12px;
}

.date {
  color: rgba(51, 51, 51, 0.75);
  font-family: Futura;
  font-size: 13px;
  font-style: normal;
  font-weight: 500;
  line-height: normal;
}

.title-container {
  padding-left: 40px;
  padding-right: 40px;
}

.title {
  color: #000;
  font-family: Futura;
  font-size: 32px;
  font-style: normal;
  font-weight: 500;
  line-height: normal;
}

.seperation-line-container {
  display: flex;
  justify-content: center;
}

.text-container {
  padding-left: 40px;
  padding-right: 40px;
  width: 780px;
  max-height: 290px;
  height: auto;
  overflow-wrap: break-word;
  word-wrap: break-word;
  word-break: break-word;
  max-lines: 12;
  overflow: hidden;
}

.voting-container-container {
  padding-left: 40px;
}

.voting-container {
  margin-top: 20px;
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  gap: 10px;
  border-radius: 10px;
  border: solid rgba(217, 217, 217, 0.50) 1.5px;
  width: 100px;
  padding: 5px;
}

img:hover {
  cursor: pointer;
}

</style>
