<template>
    <div class="flex flex-col min-w-screen min-h-screen">
        <Nav :loggedIn="false"></Nav>
        <div class="px-6 pt-6 items-center">
            <NuxtPage class="content-slot" />
        </div>
    </div>
</template>
  
<script lang="ts" setup>

// definePageMeta({
//   middleware: 'auth'
// })
</script>
  