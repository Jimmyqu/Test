<script setup>
import { reactive, ref, watch, onMounted } from 'vue'
import axios from 'axios'
const genderType = {
  1:'male',
  2:'female',
  3:'other'
}

const modalType = ref('')
const isLoading = ref(false)
const listInfo = reactive({
  list: [],
  count: 0,
  pageNum: 1,
  pageSize: 5,
})

let form = reactive({
  username:'',
  gender: ''
})

const handleSubmit = () => {
  if(form.username.trim() && form.gender) {
    isLoading.value = true;
    axios.post(modalType.value == 'add'? '/api/addUser':'/api/updateUser', {...form}).then(() => {
    }).catch(() => {
      alert('添加失败')
    }).finally( () => {
      isLoading.value = false;
      modalType.value = '';
      getListInfo(1);
    })
  } else {
    alert('plz input username and gender')
  }
}

const handleEdit = user => {
  modalType.value ='edit'
  form = {...user}
}

const handleDel =  id => {
  axios.post(`/api/deleteUser`, {
    id,
  }).then(res => {
     getListInfo(1);
  }).catch(() => {
      alert('删除失败')
  })
}

const getListInfo = (pageNum) => {
  axios.get(`/api/userList?pageNum=${pageNum}&pageSize=${listInfo.pageSize}`).then(res => {
      listInfo.list = res.data.data?.userList
      listInfo.count = res.data.data?.total
      listInfo.pageNum = res.data.data?.pageNum
  })
}

onMounted(() => {
  getListInfo(1)
})

watch(() => listInfo.pageNum, (val, oldVal) => {
  console.log(val!== oldVal)
  if(val !== oldVal) {
    getListInfo(val)
  }
})

watch(() => modalType.value, (val, oldVal) => {
  if(val == '') {
    form.username='';
    form.gender='';
  }
})

</script>

<template>
  <section>
    <div class="flex flex-start">
      <button @click="modalType='add'" class="bg-sky-500 w-[120px] outline-light-none hover:bg-sky-700">
        add
      </button>
    </div>
    <table class="table-auto min-h-[30vh]">
      <thead>
        <tr>
          <th>id</th>
          <th>name</th>
          <th>gender</th>
          <th>action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in listInfo.list" :key="item.id">
          <td>{{ item.id}}</td>
          <td>{{ item.username }}</td>
          <td>{{ genderType[item.gender] }}</td>
          <td>
            <button class="p-1 bg-green-300 text-white" @click="handleEdit(item)">edit</button>
            <button class="p-1 ml-2 bg-red-500 text-white" @click="handleDel(item.id)"> del</button>
          </td>
        </tr>
      </tbody>
    </table>
    <div class="pagination">
      <a @click="listInfo.pageNum = listInfo.pageNum - 1" href="#" class="prev" :class="listInfo.pageNum - 1 < 1 ? 'opacity-0':'opacity-100'">&laquo;</a>
      <a @click="listInfo.pageNum = i" v-for="i in  Math.ceil( listInfo.count/listInfo.pageSize)" href="#" class="page" :class="[listInfo.pageNum ===i ? 'active':'']">{{i}}</a>
      <a @click="listInfo.pageNum = listInfo.pageNum + 1" href="#" class="next" :class="listInfo.pageNum + 1 > Math.ceil( listInfo.count/listInfo.pageSize) ? 'opacity-0':'opacity-100'">&raquo;</a>
    </div>
  </section>

  <!-- Modal container -->
<div v-show="modalType" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full" id="my-modal">
  <!-- Modal -->
  <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">

    <!-- Modal header -->
    <div class="flex justify-between items-center pb-3">
      <p class="text-2xl font-bold"> {{ modalType === 'add' ? 'Add': 'Edit'}} User</p>
      <div class="modal-close cursor-pointer z-50" @click="modalType=''">
        <svg class="fill-current text-black" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 18 18">
          <path d="M12.75,6.75 L11.25,5.25 L9,7.5 L6.75,5.25 L5.25,6.75 L7.5,9 L5.25,11.25 L6.75,12.75 L9,10.5 L11.25,12.75 L12.75,11.25 L10.5,9 L12.75,6.75 Z"></path>
        </svg>
      </div>
    </div>


    <!-- Modal body -->
    <form action="#">
      <div class="mb-4">
        <label class="block text-gray-700 text-sm font-bold mb-2" for="username">
          Name:
        </label>
        <input v-model="form.username" class="bg-white  border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" id="username" maxlength="20" minlength="6" type="text" placeholder="Username">
      </div>
      <div class="mb-4">
        <label class="block text-gray-700 text-sm font-bold mb-2" for="gender">
          Gender:
        </label>
        <div class="relative">
          <select v-model="form.gender" class="block text-gray-700 appearance-none w-full bg-white border px-4 py-2 pr-8 rounded leading-tight focus:outline-none focus:shadow-outline" id="gender">
            <option value="" selected disabled hidden>Choose here</option>
            <option v-for="gender in Object.entries(genderType)" :key="gender[1]" :value="gender[0]">{{gender[1]}}</option>
          </select>
          <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700">
            <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
              <path d="M5.8,8.6 L10,13 L14.2,8.6 C14.5,8.3 15,8.5 15,9 L15,9 C15,9.5 14.5,10 14,10 L10.7,10 L10.7,10 L10,10.7 L9.3,10 L6,10 C5.5,10 5,9.5 5,9 L5,9 C5,8.5 5.5,8.3 5.8,8.6 Z"></path>
            </svg>
          </div>
        </div>
      </div>

      <!-- Modal footer -->
      <div class="flex justify-end pt-2">
        <button :disabled="isLoading" class="px-4 bg-transparent p-3 rounded-lg text-red-500 hover:bg-gray-100 hover:text-red-400 mr-2" @click.prevent="modalType=''">Cancel</button>
        <input :disabled="isLoading" class="px-4 bg-blue-500 p-3 rounded-lg text-white hover:bg-blue-400" type="submit" value="Confirm" @click.prevent="handleSubmit">
      </div>
    </form>


  </div>
</div>
</template>

<style scoped>
.pagination {
  display: inline-block;
}

.pagination a {
  color: black;
  float: left;
  padding: 8px 16px;
  text-decoration: none;
  transition: background-color .3s;
}

.pagination a.active {
  background-color: dodgerblue;
  color: white;
}

.pagination a:hover:not(.active) {background-color: #ddd;}

.prev, .next {
  margin: 0 4px;
}
</style>