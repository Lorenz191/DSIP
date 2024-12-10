<script setup>
const props = defineProps({
  arrow: {
    type: Boolean,
    required: false
  }
})

</script>

<template>
  <div class="nav-container">
    <div class="back-arrow-container">
      <a class="arrow-back" href="http://localhost:8080/landing" v-if="props.arrow"> &#60; </a>
    </div>
    <div class="search-bar-container">
      <div class="search-container">
        <input class="searchbar" placeholder="nach Begriff suchen...">
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
    <div class="user-profile-container">

    </div>
  </div>
</template>

<style scoped>
.nav-container {
  background: #2EDB7B;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: space-around;
}

.arrow-back{
  font-size: 20px;
  color: white;
  font-weight: 500;
}

.search-bar-container {
  height: 34px;
  display: flex;
  flex-direction: row;
  background: white;
  width: 800px;
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
</style>
