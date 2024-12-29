<script setup>
import { computed, onMounted, onUnmounted, reactive, ref } from 'vue'
import { RouterLink } from 'vue-router'
import { useUserStore } from '@/stores/user.js'
import ArrowDownBlack from './icons/Arrow_Down_Blackl.svg'
import ArrowDownBlue from './icons/Arrow_Down_Blue.svg'
import ArrowDownBlueFilled from './icons/Arrow_Down_Blue_Filled.svg'
import ArrowUpBlack from './icons/Arrow_Up_Black.svg'
import ArrowUpGreen from './icons/Arrow_Up_Green.svg'
import ArrowUpGreenFilled from './icons/Arrow_Up_Green_Filled.svg'
import axios from 'axios'

const currentUser = useUserStore().userUuid

const props = defineProps({
  post: {
    type: Object,
    required: true
  },
  adminView: {
    type: Boolean,
    required: false
  }
})

const status = ref(props.post.status)

const votes = reactive({
  upvotes: [...props.post.upvotes],
  downvotes: [...props.post.downvotes]
})

const upvotesCount = computed(() => votes.upvotes.length)
const downvotesCount = computed(() => votes.downvotes.length)

const date = new Date(props.post.created_at).toLocaleDateString()

const upvoted = ref(votes.upvotes.includes(currentUser))
const downvoted = ref(votes.downvotes.includes(currentUser))

const hover_up = ref(false)
const hover_down = ref(false)

const handleUpvote = () => {
  if (upvoted.value || downvoted.value) {
    votes.downvotes = votes.downvotes.filter((vote) => vote !== currentUser)
  }
  upvoted.value = !upvoted.value
  downvoted.value = false
  if (upvoted.value) {
    votes.upvotes = [...new Set([...votes.upvotes, currentUser])]
  } else {
    votes.upvotes = votes.upvotes.filter((vote) => vote !== currentUser)
  }
  send()
}

const handleDownvote = () => {
  hover_up.value = false
  if (!downvoted.value) {
    downvoted.value = true
    upvoted.value = false
    votes.downvotes.push(currentUser)
    votes.upvotes = votes.upvotes.filter((vote) => vote !== currentUser)
  } else {
    downvoted.value = false
    votes.downvotes = votes.downvotes.filter((vote) => vote !== currentUser)
  }
  send()
}

const send = () => {
  try {
    axios
      .post('http://localhost:8000/api/post/vote/', {
        post_id: props.post._id,
        votes: votes
      })
      .then((response) => {
        console.log(response)
      })
  } catch (error) {
    console.error('Error voting:', error)
  }
}

const deletePost = () => {
  try {
    axios
      .post('http://localhost:8000/api/post/delete/', {
        post_id: props.post._id
      })
      .then((response) => {
        console.log(response)
      })
  } catch (error) {
    console.error('Error deleting post:', error)
  }
}

let socket

onMounted(() => {
  socket = new WebSocket('ws://localhost:8000/ws/votes/')

  socket.onopen = () => {
    console.log('WebSocket connection opened')
  }

  socket.onmessage = (event) => {
    console.log('Message from server ', event.data)
    const data = JSON.parse(event.data)
    if (data.post_id !== props.post._id) {
      return
    }
    votes.upvotes = data.upvotes
    votes.downvotes = data.downvotes
  }

  socket.onerror = (error) => {
    console.error('WebSocket error:', error)
  }

  socket.onclose = (event) => {
    console.log('WebSocket closed:', event)
  }
})

onUnmounted(() => {
  if (socket) {
    socket.close()
  }
})
</script>

<template>
  <div class="main-container">
    <div class="post-container">
      <div class="date-container">
        <p class="date">Veröffentlicht am {{ date }}</p>
        <div class="status-del-div">
          <p class="del-symbol" v-if="adminView" @click="deletePost">&#x1F5D1;</p>
          <p class="status">{{ status }}</p>
        </div>
      </div>
      <RouterLink :to="`/post/${props.post._id}`">
        <div class="title-container">
          <h1 class="title">{{ props.post.body.title }}</h1>
        </div>
        <div class="seperation-line-container">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="720"
            height="4"
            viewBox="0 0 720 4"
            fill="none"
          >
            <path
              d="M2 2H699.5"
              stroke="#333333"
              stroke-opacity="0.2"
              stroke-width="3"
              stroke-linecap="round"
            />
          </svg>
        </div>
        <div class="text-container">
          <p class="post-body">
            {{ props.post.body.content }}
          </p>
        </div>
      </RouterLink>
      <div class="seperation-line-container">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="720"
          height="4"
          viewBox="0 0 720 4"
          fill="none"
        >
          <path
            d="M2 2H699.5"
            stroke="#333333"
            stroke-opacity="0.2"
            stroke-width="3"
            stroke-linecap="round"
          />
        </svg>
      </div>
      <div class="voting-container-container">
        <div class="voting-container">
          <div class="upvote">
            <p>
              {{ upvotesCount }}
            </p>
            <img
              :src="upvoted ? ArrowUpGreenFilled : hover_up ? ArrowUpGreen : ArrowUpBlack"
              alt="upvote"
              style="height: 36px"
              @click="handleUpvote"
              @mouseover="hover_up = true"
              @mouseleave="hover_up = false"
            />
          </div>
          <div class="vertical-seperation-line">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="2"
              height="36"
              viewBox="0 0 2 36"
              fill="none"
            >
              <path
                d="M1 1V34.5"
                stroke="#D9D9D9"
                stroke-opacity="0.5"
                stroke-width="1.5"
                stroke-linecap="round"
              />
            </svg>
          </div>
          <div class="downvote">
            <p>
              {{ downvotesCount }}
            </p>
            <img
              :src="downvoted ? ArrowDownBlueFilled : hover_down ? ArrowDownBlue : ArrowDownBlack"
              alt="upvote"
              style="height: 36px"
              @click="handleDownvote"
              @mouseover="hover_down = true"
              @mouseleave="hover_down = false"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.main-container{
  padding:10px;
}

.post-container {
  margin-bottom: 60px;
  width: 800px;
  height: auto;
  padding-bottom: 10px;
  box-shadow: 2px 2px 5px 0px rgba(0, 0, 0, 0.25);
  border-radius: 20px;
  border: 3px solid rgba(217, 217, 217, 0.2);
  background: #fff;
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
  border: solid rgba(217, 217, 217, 0.5) 1.5px;
  width: fit-content;
  padding: 5px;
}

img:hover {
  cursor: pointer;
}

.upvote,
.downvote {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 2px;
}

.status-del-div {
  display: flex;
  flex-direction: row;
  gap: 5px;
}

.del-symbol:hover {
  cursor: pointer;
}
</style>
