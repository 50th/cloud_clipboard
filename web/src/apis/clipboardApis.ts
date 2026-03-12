import request from '@/apis/axiosInstance'

const apiPrefix = '/api/clipboard'

export async function getClipboardListApi(params?: any): Promise<any> {
  return request.get(`${apiPrefix}/clipboards/`, { params })
}

export async function addClipboardApi(data): Promise<any> {
  return request.post(`${apiPrefix}/clipboards/`, data)
}

export async function getClipboardApi(id?: number | string): Promise<any> {
  return request.get(`${apiPrefix}/clipboards/${id}/`)
}

export async function editClipboardApi(id: number | string, data): Promise<any> {
  return request.put(`${apiPrefix}/clipboards/${id}/`, data)
}

export async function delClipboardListApi(id: number): Promise<any> {
  return request.delete(`${apiPrefix}/clipboards/${id}/`)
}
