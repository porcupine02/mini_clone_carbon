<template>
    <div class="max-w-xl mx-auto bg-gray-50 p-6 rounded-lg shadow-md border border-gray-200">
      <h2 class="text-2xl font-semibold mb-4 text-gray-800">{{ props.title }}</h2>
      <h3 class="text-base font-medium text-gray-600 mb-6">{{ props.description }}</h3>
  
      <!-- Read-only content slot -->
      <div class="space-y-4">
        <slot />
      </div>
  
      <!-- Back Button -->
      <div class="mt-8 flex justify-end">
        <button
          type="button"
          class="bg-gray-300 text-gray-800 py-2 px-4 rounded-md hover:bg-gray-400 transition"
          @click="() => router.back()"
        >
          Back
        </button>
      </div>
    </div>
  </template>
  
  <script setup>
  const router = useRouter()
  
  const props = defineProps({
    title: {
      type: [String],
      default: 'Title Form',
    },
    description: {
      type: [String],
      default: 'Description Form',
    },
  })
  </script>
  