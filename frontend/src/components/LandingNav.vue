<script setup>
import AuthService from '@/auth/AuthService.js'
import {onMounted, onUnmounted, ref, watch} from "vue";
import {useRouter} from "vue-router";
import UserIconSmall from "@/components/User/UserIconSmall.vue";
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
const auth = new AuthService()

const logOut = () => {
  auth.logout()
}
const emit = defineEmits(['update:searchQuery'])

const screenWidth = ref(window.innerWidth);

const updateScreenWidth = () => {
  screenWidth.value = window.innerWidth;
};

const searchInput = ref('')

const onInput = (event) => {
  searchInput.value = event.target.value
  emit('update:searchQuery', searchInput.value)
}

onMounted(() => {
  window.addEventListener('resize', updateScreenWidth);
});

onUnmounted(() => {
  window.removeEventListener('resize', updateScreenWidth);
});

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
      <button @click="logOut" v-if="props.logout">Abmelden</button>
    </div>

    <div class="search-bar-container" v-if="props.searchbar">
      <div class="search-container">
        <input @input="onInput" :value="searchInput" class="searchbar" placeholder="nach Begriff suchen...">
      </div>
      <div class="icon-container">
        <div class="search-icon-container">
          <img src="./icons/SearchIcon2.svg" class="icon" alt="search-icon" style="height: 25px;">
        </div>
        <div class="filter-icon-container">
          <img src="./icons/Filter.svg" class="icon" alt="filter-icon" style="background: transparent; height: 25px;">
        </div>
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

.icon-container {
  display: flex;
  flex-direction: row;
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
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.small-nav-container .search-bar-container {
  width: 70vw;
}


button{
  font-size: 20px;
  font-weight: bold;
  color: white;
}

button:hover{
  text-decoration: underline;
}

</style>
