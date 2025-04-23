<template>
    <Nav :loggedIn="true"></Nav>
    <Assignment :status="'submit'"></Assignment>
    <div class="bg-red-300">
      <h2>API Data:</h2>
      <ul>
        <li v-for="response in fieldResponses" :key="response.id">
          {{ response.first_name }}
        </li>
      </ul>
    </div>
    <div>
  
      <FormTextField label="Email Address" placeholder="you@example.com" type="email" />
      <FormSelectField label="Role" :options="[
        { value: 'student', label: 'Student' },
        { value: 'teacher', label: 'Teacher' },
        { value: 'admin', label: 'Admin' }
      ]" />
      <FormFileUploadField label="Upload File" @update:file="onFileUpload" />
    </div>
    <div class="my-6">
      <FormBase>
        <FormTextField label="Email Address" placeholder="you@example.com" type="email" />
  
  
      </FormBase>
    </div>
  </template>
  
  <script lang="ts" setup>
  // import Card from 'primevue/card';
  import Card from 'primevue/card';
  
  import { ref, onMounted } from 'vue'
  import axios from 'axios'
  const config = useRuntimeConfig()
  
  const apiUrl = config.public.baseUrl || 'http://localhost:8000'
  // const test = process
  interface FieldResponse {
    id: number;
    first_name: string;
    // Add other fields if necessary
  }
  const file = ref(null)
  function onFileUpload(uploadedFile: any) {
    file.value = uploadedFile
  }
  const fieldResponses = ref<FieldResponse[]>([])
  
  onMounted(async () => {
    try {
      console.log('apiUrl', apiUrl)
      // const response = await axios.get(`${apiUrl}/auth/test`)
      const response = await axios.get('http://localhost:8000/auth/test/')
      // console.log("response2", response2.data)
      fieldResponses.value = response.data
      console.log('fieldResponses', fieldResponses.value)
    } catch (error) {
      console.error('Error fetching data:', error)
    }
  })
  </script>
  