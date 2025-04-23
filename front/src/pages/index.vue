<template>
  <div>
    <p>Own Subject: {{ ownSubject }}</p>
    <p>Own Project: {{ ownProject }}</p>

    <!-- Navigation Buttons -->
    <div class="bg-blue-300 flex flex-wrap gap-2 p-4">
      <div class="p-2 bg-blue-300 hover:bg-blue-500 cursor-pointer" @click="navigateTo('/subject/detail-1/project/create')">
        Create Project
      </div>
      <div class="p-2 bg-blue-300 hover:bg-blue-500 cursor-pointer" @click="navigateTo('/subject/create')">
        Create Subject
      </div>
      <div class="p-2 bg-blue-300 hover:bg-blue-500 cursor-pointer" @click="navigateTo('/form/create')">
        Create Form
      </div>
      <div class="p-2 bg-blue-300 hover:bg-blue-500 cursor-pointer" @click="navigateTo('/form/link')">
        Link Form & Subject
      </div>
      <div class="p-2 bg-blue-300 hover:bg-blue-500 cursor-pointer" @click="navigateTo('/form/detail-20')">
        Form Detail Preview
      </div>
      <div class="p-2 bg-blue-300 hover:bg-blue-500 cursor-pointer" @click="navigateTo('/dashboard')">
        Dashboard
      </div>
      <div class="p-2 bg-blue-300 hover:bg-blue-500 cursor-pointer" @click="navigateTo('/subject/detail-1/project/9')">
        Project Detail
      </div>
      <div v-if="ownProject && ownSubject" class="p-2 bg-blue-300 hover:bg-blue-500 cursor-pointer"
           @click="navigateTo(`/subject/detail-${ownSubject}/project/${ownProject}`)">
        My Project Detail
      </div>
    </div>

    <!-- Subjects Grid -->
    <div v-if="Array.isArray(subjects) && subjects.length > 0"
         class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 p-4">
      <div v-for="subject in subjects" :key="subject.id"
           class="bg-green-200 rounded-2xl shadow-md p-4 cursor-pointer hover:bg-green-300"
           @click="navigateTo(`/subject/detail-${subject.id}/project/create`)">
        <h2 class="text-lg font-semibold">{{ subject.name }}</h2>
        <p class="text-base text-gray-700">{{ subject.description }}</p>
      </div>
    </div>
  </div>
</template>


<script lang="ts" setup>
import type { SubjectResponse } from '../types/interface';
// import { navigateTo } from '#app'
const router = useRouter()

const auth = useAuthStore()

const user = computed(() => auth.user)
const accessToken = computed(() => auth.accessToken)
const ownProject = computed(() => auth.ownProject)
const ownSubject = computed(() => auth.ownSubject)


const subjects = ref<SubjectResponse[]>([])
const getAllSubjects = async () => {
  try {
    const res = await useFetch(
      'http://localhost:8000/form/subject',
      {
        method: 'GET',
        headers: {
          Authorization: `Bearer ${accessToken.value}`,
        },
      }
    )
    subjects.value = res.data.value as SubjectResponse[];
  } catch (error) {
    console.error('Request failed:', error);
  }
}
onMounted(async () => {
  if (!auth.user || !auth.accessToken || !auth.refreshToken) {
    auth.loadFromCookies()
  }
  await getAllSubjects()
})

const navigateTo = (path: string) => {
  router.push(path)
}
</script>
