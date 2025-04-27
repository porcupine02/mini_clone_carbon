<template>
  <nav class="flex items-center justify-between px-6 py-4 bg-white shadow-md">
    <!-- Logo -->
    <div class="flex flex-row gap-6">
      <div class="text-xl font-bold text-gray-800">
        <NuxtLink to="/">MyLogo</NuxtLink>
      </div>
      <div v-if="auth.user?.role == 'Admin'" class="text-xl font-bold text-gray-800">
        <NuxtLink to="/subject/create">Create Subject</NuxtLink>
      </div>
      <div v-if="['Admin', 'Teacher'].includes(auth.user?.role ?? '')" class="text-xl font-bold text-gray-800">
        <NuxtLink to="/form/create">Create Form</NuxtLink>
      </div>
      <div v-if="['Admin', 'Teacher'].includes(auth.user?.role ?? '')" class="text-xl font-bold text-gray-800">
        <NuxtLink to="/form/link">Link Form & Subject</NuxtLink>
      </div>
      <div v-if="['Admin', 'Teacher'].includes(auth.user?.role ?? '')" class="text-xl font-bold text-gray-800">
        <NuxtLink to="/dashboard">Dashboard</NuxtLink>
      </div>


    </div>


    <!-- Right Side -->
    <div>
      <div v-if="loggedIn" class="flex items-center gap-4">
        <span class="text-gray-700">Hello, {{ user?.username }}</span>
        <button @click="handleLogout" class="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600">
          Logout
        </button>
      </div>
      <div v-else>
        <NuxtLink to="/login" class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
          Login
        </NuxtLink>
      </div>
    </div>
  </nav>
</template>
  
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '@/composables/useAuth'
// import { useAuthStore } from '@/stores/auth'

const { logout } = useAuth()
// const authStore = useAuthStore()
const loggedIn = ref(false)
const user = ref<Record<string, any> | null>(null)

const router = useRouter()
const auth = useAuthStore()


const getAuth = async () => {
  auth.loadFromCookies()
}
onMounted(async () => {

  await getAuth();
  const access_token = useCookie('access_token').value
  const user_cookie = useCookie('user').value
  if (access_token && user_cookie) {
    loggedIn.value = true
    try {
      user.value = JSON.parse(user_cookie)
    } catch {
      user.value = null
    }
  } else {
    loggedIn.value = false
    user.value = null
  }
})

const handleLogout = () => {
  logout()
  loggedIn.value = false
  user.value = null
  router.push('/login')
}
</script>
