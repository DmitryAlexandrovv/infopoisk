<script setup>
  import { ref, reactive } from 'vue'

  const vueData = reactive({pages: [], searchValue: ''});

  const handleSubmit = () => {
        fetch('http://localhost:5000/search', {
          method: 'POST',
            body: JSON.stringify({
              query: vueData.searchValue,
            }),
            headers: {
              'Content-type': 'application/json',
            }
          })
            .then((res) => res.json())
            .then((data) => {
              console.log(data);
              vueData.pages = data
            });
  }
</script>

<template>
  <div>
    <input type="text" v-model="vueData.searchValue" />
    <button @click=handleSubmit>Поиск</button>

    <div class="pages"> 
      <div v-for="page in vueData.pages" :key="page[0]">
          <a 
            :href="`http://localhost:5000/page?page=${page[0]}`"
            target="blank"
          >
            {{page[1]}}
          </a>
        </div>
    </div>
  </div>
</template>

<style scoped>
</style>
