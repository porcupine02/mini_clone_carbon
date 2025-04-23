<template>
  <div class="max-w-2xl mx-auto py-10">
    <h1 class="text-2xl font-bold mb-6">Create Project</h1>

    <form @submit.prevent="submitForm" class="space-y-4">
      <!-- Title (TH) -->
      <div>
        <label class="block font-medium mb-1">Project Title (TH)</label>
        <input v-model="form.title_th" type="text" class="w-full border rounded-lg p-2" required />
      </div>

      <!-- Title (EN) -->
      <div>
        <label class="block font-medium mb-1">Project Title (EN)</label>
        <input v-model="form.title_en" type="text" class="w-full border rounded-lg p-2" required />
      </div>

      <!-- Keywords -->
      <div>
        <label class="block font-medium mb-1">Keywords (comma-separated)</label>
        <input v-model="form.keywordText" type="text" class="w-full border rounded-lg p-2"
          placeholder="e.g. hello, world" />
      </div>

      <!-- Teacher -->
      <label class="block font-medium mb-1">Teacher</label>
      <select v-model="form.teacher" class="w-full border rounded-lg p-2" required>
        <option disabled value="">Please select a teacher</option>
        <option v-for="teacher in teachers" :key="teacher.id" :value="teacher.id">
          {{ `${teacher.first_name} ${teacher.last_name}` }}
        </option>
      </select>

      <!-- Submit -->
      <button type="submit" class="bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-blue-700">
        Create Project
      </button>
    </form>
  </div>
</template>
  
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import type { ProjectResponse } from '~/src/types/interface';
import type { User } from '~/src/types/authInterface';

const route = useRoute()
const user = ref()

const teachers = ref<User[]>([])


const accessToken = ref('')
// Form state
const form = ref({
  title_th: '',
  title_en: '',
  keywordText: '',
  teacher: 0,
})


const getAuth = async () => {
  accessToken.value = localStorage.getItem('access_token') ?? ''
  const rawUser = localStorage.getItem('user')
  user.value = rawUser ? JSON.parse(rawUser) : null
}
onMounted(async () => {

  await getAuth();
  const res = await useFetch(`http://localhost:8000/auth/teachers`, {
    method: 'GET',
    headers: {
      Authorization: `Bearer ${accessToken.value}`
    }
  })
  teachers.value = res.data.value as User[]

  // TODO: Get main form of subject
  //   accessToken.value = localStorage.getItem('access_token') || ''
  //   console.log('assecc ', accessToken)
  //   // Fetch subjects from backend
  //   subjects.value = await useFetch(`http://localhost:8000/form/subject`, {
  //     method: 'GET',
  //     headers: {
  //       Authorization: `Bearer ${accessToken.value}`
  //     }

  //   })
})

const submitForm = async () => {
  const payload = {
    title_th: form.value.title_th,
    title_en: form.value.title_en,
    keyword: form.value.keywordText
      .split(',')
      .map((kw) => kw.trim())
      .filter(Boolean),
    subject: route.params.subj_id,
    student: user.value.id,
    teacher: form.value.teacher,
    created_by: user.value.id,
    updated_by: user.value.id,
  }

  try {
    console.log('payload', payload)
    const accessToken = localStorage.getItem('access_token')

    console.log('accessToken', accessToken)
    const res = await useFetch<ProjectResponse>(`http://localhost:8000/project/`, {
      method: 'POST',
      body: payload,
      headers: {
        Authorization: `Bearer ${accessToken}`
      }

    })
    // console.log("res", res.data.value?.id)
    navigateTo(`/subject/detail-${res.data.value?.subject}/project/${res.data.value?.id}`)
  } catch (err) {
    console.error('Project creation failed:', err)
    alert('Project creation failed')
  }
}


</script>
  