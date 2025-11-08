'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { UploadDropzone } from '@/components/upload/UploadDropzone'

export default function UploadPage() {
  const router = useRouter()
  const [isUploading, setIsUploading] = useState(false)
  const [selectedFiles, setSelectedFiles] = useState<File[]>([])

  const handleFileSelect = (files: File[]) => {
    setSelectedFiles(files)
  }

  const handleFileUpload = async () => {
    if (selectedFiles.length === 0) {
      alert('업로드할 파일을 선택해주세요.')
      return
    }

    setIsUploading(true)
    try {
      const formData = new FormData()
      selectedFiles.forEach((file) => {
        formData.append('files', file)
      })

      const response = await fetch('http://localhost:8000/api/upload/resume', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) throw new Error('Upload failed')

      const data = await response.json()
      // 세션 ID와 첫 질문 저장
      localStorage.setItem('session_id', data.session_id)
      localStorage.setItem('first_question', data.first_question)

      // 채팅 페이지로 이동
      router.push('/chat')
    } catch (error) {
      console.error('Upload error:', error)
      alert('업로드 중 오류가 발생했습니다.')
    } finally {
      setIsUploading(false)
    }
  }

  return (
    <main className="container mx-auto px-4 py-16">
      <div className="max-w-2xl mx-auto space-y-8">
        <div className="text-center">
          <h1 className="text-3xl font-bold mb-4">이력서 업로드</h1>
          <p className="text-muted-foreground">
            PDF 이력서를 업로드하면 AI가 분석하여 더 나은 이력서를 만들어드립니다.
          </p>
        </div>

        <UploadDropzone
          onFileSelect={handleFileSelect}
          isUploading={isUploading}
          selectedFiles={selectedFiles}
        />

        {selectedFiles.length > 0 && (
          <div className="flex justify-center">
            <button
              onClick={handleFileUpload}
              disabled={isUploading}
              className={`
                px-8 py-3 rounded-lg font-medium
                ${isUploading
                  ? 'bg-gray-300 cursor-not-allowed'
                  : 'bg-primary text-primary-foreground hover:bg-primary/90'
                }
              `}
            >
              {isUploading ? '업로드 중...' : '업로드 시작'}
            </button>
          </div>
        )}

        <div className="text-sm text-muted-foreground text-center">
          <p>지원 형식: PDF (여러 파일 업로드 가능)</p>
          <p>최대 파일 크기: 10MB</p>
        </div>
      </div>
    </main>
  )
}
