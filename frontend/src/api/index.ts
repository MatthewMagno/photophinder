export type Photo = {
  id: string
  thumb_key: string
  preview_key: string
  original_key: string
  caption?: string | null
  objects?: string[] | null
}

export type Face = {
  id: string
  bounding_box: { x1: number; y1: number; x2: number; y2: number }
  person_name?: string | null
}

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export async function fetchPhotos(): Promise<Photo[]> {
  const res = await fetch(`${API_BASE}/photos`)
  return res.json()
}

export async function searchPhotos(query: string): Promise<Photo[]> {
  const res = await fetch(`${API_BASE}/search?query=${encodeURIComponent(query)}`)
  return res.json()
}

export async function uploadPhoto(file: File): Promise<Photo> {
  const formData = new FormData()
  formData.append('file', file)
  const res = await fetch(`${API_BASE}/photos/upload`, { method: 'POST', body: formData })
  return res.json()
}

export async function fetchFaces(photoId: string): Promise<Face[]> {
  const res = await fetch(`${API_BASE}/faces/photo/${photoId}`)
  return res.json()
}

export async function labelFace(faceId: string, displayName: string): Promise<void> {
  await fetch(`${API_BASE}/faces/${faceId}/label`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ display_name: displayName })
  })
}

export function buildImageUrl(key: string): string {
  const base = import.meta.env.VITE_STORAGE_BASE || 'http://localhost:9000/photophinder'
  return `${base}/${key}`
}
