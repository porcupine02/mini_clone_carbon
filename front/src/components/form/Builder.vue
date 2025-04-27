<template>
  <div class="p-4 grid grid-cols-1 md:grid-cols-2 gap-6">

    <!-- Preview Form -->
    <div>
      <h3 class="text-lg font-semibold mt-6">Form Preview</h3>
      <FormBase class="space-y-4 mt-2" :title="props.pre_title" :description="props.pre_des">
        <div v-for="(field, index) in fields" :key="'preview-' + index">
          <label class="block font-medium mb-1">{{ field.label }}</label>
          <FormTextField v-if="field.type === 'text'" />
          <FormSelectField v-else-if="field.type === 'select'" :options="getOptions(field)" />
          <FormFileUploadField v-else-if="field.type === 'file'" />
        </div>
      </FormBase>

    </div>

    <!-- Manage Form -->
    <div>
      <h2 class="text-xl font-bold mb-4">Form Builder</h2>
      <div class="space-y-4">
        <div v-for="(field, index) in fields" :key="index" class="p-4 border rounded space-y-2">
          <input v-model="field.label" placeholder="Label" class="w-full p-2 border rounded" />
          <select v-model="field.type" class="w-full p-2 border rounded">
            <option value="text">Text Field</option>
            <option value="select">Select Field</option>
            <option value="file">Upload File</option>
          </select>

          <div v-if="field.type === 'select'">
            <input v-model="field.optionRaw" placeholder="Options (comma separated)" class="w-full p-2 border rounded" />
          </div>

          <button @click="removeField(index)" class="text-red-500">Remove</button>
        </div>

        <button @click="addField" class="px-4 py-2 bg-blue-500 text-white rounded">Add Field</button>
      </div>

    </div>

  </div>
</template>
  
<script setup lang="ts">
import { ref } from 'vue'

const fields = ref<any[]>([])
const props =
  defineProps({
    pre_title: {
      type: String,
      default: '',
    },
    pre_des: {
      type: String,
      default: '',
    },
  })
const addField = () => {
  fields.value.push({
    label: '',
    type: 'text',
    optionRaw: ''
  })
}

const removeField = (index: number) => {
  fields.value.splice(index, 1)
}

const getOptions = (field: any) => {

  return field.optionRaw?.split(',')
    .map((opt: string) => opt.trim())
    .filter((opt: string) => opt.length > 0)
    .map((opt: string) => ({ label: opt, value: opt })) || []
}

const emit = defineEmits(['update:fields'])
watch(fields, (newFields) => {
  emit('update:fields', newFields)
}, { deep: true })
</script>
  