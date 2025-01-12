<script setup>
import {ref} from "vue";

const easynameUrl = ref('https://www.easyname.at/de/unternehmen/presse\n')
</script>

<template>
  <div class="sponsor">
    <p>Powered by <a :href="easynameUrl" target="_blank"><img src="https://static.easyname.com/images/svg/singles/logos/easyname/easyname_logo_default.svg?v=2" height="40" alt=""></a></p>
  </div>
</template>

<style scoped>
*{
  font-family: Futura,sans-serif;
}
.sponsor {
  display: flex;
  justify-content: center;
  flex-direction: row;
}
</style>
