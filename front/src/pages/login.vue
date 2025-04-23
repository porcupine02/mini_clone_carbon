<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100">
    <div class="w-full max-w-md bg-white p-8 rounded-xl shadow-md">
      <h2 class="text-2xl font-bold text-center text-gray-800 mb-6">Login</h2>

      <form class="space-y-4" @submit="handleLogin">
        <!-- Username -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Usernmae</label>
          <input type="text" v-model="username"
            class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="you@example.com" />
        </div>

        <!-- Password -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Password</label>
          <input type="password" v-model="password"
            class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="••••••••" />
        </div>

        <!-- Login Button -->

        <button type="submit"
          class="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 rounded-lg transition duration-200">
          Log In
        </button>
      </form>

      <!-- Signup Link -->
      <p class="mt-4 text-center text-sm text-gray-600">
        Don't have an account?
        <NuxtLink to="/register" class="text-blue-600 hover:underline">Sign up</NuxtLink>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">

import { useAuth } from '@/composables/useAuth'

const username = ref('')
const password = ref('')
const { login } = useAuth()

definePageMeta({
  layout: 'homepage',
});
const handleLogin = async (e: Event) => {

  e.preventDefault()
  console.log('handle Login')
  const credentials = {
    username: username.value,
    password: password.value
  }

  console.log('credentials', credentials)
  const result = await login(credentials)

  console.log('result', result)

  // Check if login was successful
  if (result.success) {
    navigateTo('/') // Redirect to the dashboard or home page
  } else {
    // Handle error (you could show an error message)
    alert('Login failed. Please check your credentials.')
  }
}
</script>