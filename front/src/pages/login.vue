<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100">
    <div class="w-full max-w-md bg-white p-8 rounded-xl shadow-md">
      <h2 class="text-2xl font-bold text-center text-gray-800 mb-6">Login</h2>

      <form class="space-y-4" @submit="handleLogin">
        <!-- Username -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Username
          </label>

          <input type="text" v-model="username"
            class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="you@example.com" />

          <p v-if="credentialsValidationErrorForm.username" class="text-red-500 text-sm mt-1">{{
            credentialsValidationErrorForm.username }}</p>
        </div>

        <!-- Password -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Password
          </label>
          <input type="password" v-model="password"
            class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="••••••••" />

          <p v-if="credentialsValidationErrorForm.password" class="text-red-500 text-sm mt-1">{{
            credentialsValidationErrorForm.password }}</p>
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
import {
  LoginSchema
} from '@/utils/formValidator';
const username = ref('')
const password = ref('')
const { login } = useAuth()
type validateLogin = {
  username: string,
  password: string
}
const credentialsValidationErrorForm = reactive<validateLogin>({
  username: "",
  password: ""
});
definePageMeta({
  layout: 'homepage',
});
const handleLogin = async (e: Event) => {

  e.preventDefault()
  const credentials = {
    username: username.value,
    password: password.value
  }


  const validate = LoginSchema.validate(credentials, {
    abortEarly: false,
  });
  console.log('validate', validate)

  if (validate.error) {
    credentialsValidationErrorForm.username = "";
    credentialsValidationErrorForm.password = "";

    validate.error.details.forEach((err) => {
      if (err.path.includes("username")) {
        credentialsValidationErrorForm.username = err.message;
      }
      if (err.path.includes("password")) {
        credentialsValidationErrorForm.password = err.message;
      }
    });

    return;
  }
  const result = await login(credentials)



  if (result.success) {
    navigateTo('/')
  } else {
    alert('Login failed. User or Password incorrect.')
  }
}
</script>