import request from '@/apis/axiosInstance'

const apiPrefix = '/api/clipboard'

export async function getClipboardListApi() {
  return request.get(`${apiPrefix}/clipboards/`)
}
