<script setup>
import {onMounted, onUnmounted, ref, watch} from "vue";
import {useRouter} from "vue-router";
import UserIconSmall from "@/components/User/UserIconSmall.vue";
import LogoutButton from '@/components/Buttons/logout-button.vue'
const props = defineProps({
  arrow: {
    type: Boolean,
    required: false
  },
  logout: {
    type: Boolean,
    required: false
  },
  searchbar:{
    type: Boolean,
    required: false
  },
  profileIcon:{
    type:Boolean,
    required:false
  }
})
const router = useRouter();
const emit = defineEmits(['update:searchQuery'])

const screenWidth = ref(window.innerWidth);
const small = ref(screenWidth.value < 700);

const updateScreenWidth = () => {
  screenWidth.value = window.innerWidth;
};

const search = () => {
  searchInput.value = searchInput.value.toString().toLowerCase();
  emit("search", searchInput.value)
}


onMounted(() => {
  window.addEventListener('resize', updateScreenWidth);
});

onUnmounted(() => {
  window.removeEventListener('resize', updateScreenWidth);
});

const searchInput = ref('')

const onInput = (event) => {
  searchInput.value = event.target.value
  emit('update:searchQuery', searchInput.value)
}


const backToLanding = () => {
    router.push({name: 'landing'});
}

watch(() => props.modelValue, (newVal) => {
  searchInput.value = newVal
})


</script>

<template>
  <div :class="[{'nav-container' : screenWidth>700}, {'small-nav-container' : screenWidth<700}]">

    <div class="back-arrow-container icon">
      <img src="../components/icons/Arrow_back.svg" alt="arrow_back" v-if="props.arrow" @click="backToLanding" >
      <logout-button v-if="logout" :small="small"></logout-button>
    </div>

    <div class="search-bar-container" v-if="props.searchbar">
      <div class="search-container">
        <input @input="onInput" :value="searchInput" class="searchbar" placeholder="nach Begriff suchen...">

      </div>
    </div>
    <div class="user-profile-container" v-if="props.profileIcon">
      <UserIconSmall></UserIconSmall>
    </div>
  </div>
</template>

<style scoped>
.nav-container {
  background: #2EDB7B;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}


.back-arrow-container {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  padding-left: 25px;
}

.search-bar-container {
  height: 34px;
  display: flex;
  flex-direction: row;
  background: white;
  width: 70vw;
  justify-content: space-between;
  align-items: center;
  border-radius: 10px;
  padding-left: 6px;
  padding-right: 6px;
}

.search-container {
  width: 95%;
}

.searchbar {
  width: 100%;
}

.searchbar:focus {
  outline: none;
}

.icon:hover {
  cursor: pointer;
}

.user-profile-container {
  padding-right: 25px;
}

.small-nav-container {
  background: #2EDB7B;
  height: 80px;
  gap: 5px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.small-nav-container .search-bar-container {
  width: 70vw;
}


button{
  font-size: 15px;
  font-weight: bold;
  color: white;
}

button:hover{
  text-decoration: underline;
}

</style>
