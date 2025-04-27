<template>
  <div class="flex items-center justify-center">

    <div class="w-[800px]">
      <h1 class="text-2xl font-bold mb-8 text-center">Submissions From Students</h1>

      <div v-if="submissions.length === 0" class="text-center p-6 mt-6 text-gray-500">
        No submission found.
      </div>

      <div v-else class="w-full space-y-6 items-center">
        <!-- <div> -->
        <div v-for="submission in submissions" :key="submission.id"
          class="w-full p-6 border rounded-lg shadow hover:shadow-md transition bg-white flex justify-between items-center">
          <!-- Left -->
          <div class="flex flex-col">
            <div class="flex items-center text-xl font-semibold space-x-2">
              <div>{{ submission.form.title }} /</div>
            </div>

            <div class="mt-2 ml-3 text-gray-600 space-y-1">
              <p>
                <strong>Project : </strong> {{ submission.project.title_th }} / {{ submission.project.title_en }}
              </p>
              <p>
                <strong>Student : </strong> {{ submission.project.student_detail.first_name }} {{
                  submission.project.student_detail.last_name }}
              </p>
              <p>
                <strong>Subject : </strong> {{ submission.project.subject_detail.name }}
              </p>
              <p>
                <strong>Status : </strong>
                <span :class="{
                  'text-yellow-500': submission.status === 'Pending',
                  'text-green-500': submission.status === 'Approved',
                  'text-red-500': submission.status === 'Rejected'
                }">
                  {{ submission.status }}
                </span>
              </p>
            </div>
          </div>

          <!-- Right -->
          <div class="ml-6 space-y-2">

            <div class="bg-blue-500 text-center text-white px-5 py-2 rounded hover:bg-blue-600 whitespace-nowrap"
              @click="navigateTo(`/subject/detail-${submission.project.subject_detail.id}/project/${submission.project.id}/form-${submission.form.id}`)">
              View detail
            </div>
            <div class="bg-green-500 text-center text-white px-5 py-2 rounded hover:bg-blue-600 whitespace-nowrap"
              @click="updateStatus(submission.id, 'Approved')">
              Approve
            </div>
            <div class="bg-red-500 text-center text-white px-5 py-2 rounded hover:bg-blue-600 whitespace-nowrap"
              @click="updateStatus(submission.id, 'Rejected')">
              Reject
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup lang="ts">
import { useRoute } from 'vue-router'
import { ref, onMounted } from 'vue'
import type { AssignmentTeacherResponse } from '~/src/types/interface';

const route = useRoute()
const subjectId = route.query.subjectId;
const submissions = ref<AssignmentTeacherResponse[]>([])
const auth = useAuthStore()

const getAuth = async () => {
  auth.loadFromCookies()
}

onMounted(async () => {
  await getAuth();
  await getAssiments()

})

const getAssiments = async () => {
  try {
    const res = await useFetch(
      `http://localhost:8000/project/subject/assignment-teacher/${subjectId}`,
      {
        method: 'GET',
        headers: {
          Authorization: `Bearer ${auth.accessToken}`,
        },
      }
    )
    console.log('res.data.value', res.data.value)
    console.log('submissions', submissions.value)
    submissions.value = [...(res.data.value as AssignmentTeacherResponse[])];

    console.log('submissions 2', submissions.value)

  } catch (error) {
    console.error('Request failed:', error);
  }
}

const updateStatus = async (submissionId: number, status: string) => {
  try {
    const payload = {
      status: status,
      approve_by_id: auth.user?.id
    }
    const res = await useFetch(
      `http://localhost:8000/project/submission/${submissionId}`,
      {
        method: 'PATCH',
        headers: {
          Authorization: `Bearer ${auth.accessToken}`,
        },
        body: payload
      }
    )
    // submissions.value = res.data.value as AssignmentTeacherResponse[];
    await getAssiments();
  } catch (error) {
    console.error('Request failed:', error);
  }
}
</script>
  