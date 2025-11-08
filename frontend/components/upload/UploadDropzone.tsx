'use client'

import { useCallback } from 'react'
import { useDropzone } from 'react-dropzone'

interface UploadDropzoneProps {
  onFileSelect: (files: File[]) => void
  isUploading: boolean
  selectedFiles?: File[]
}

export function UploadDropzone({ onFileSelect, isUploading, selectedFiles = [] }: UploadDropzoneProps) {
  const onDrop = useCallback(
    (acceptedFiles: File[]) => {
      if (acceptedFiles.length > 0) {
        onFileSelect(acceptedFiles)
      }
    },
    [onFileSelect]
  )

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
    },
    multiple: true,
    disabled: isUploading,
  })

  return (
    <div
      {...getRootProps()}
      className={`
        border-2 border-dashed rounded-lg p-12 text-center cursor-pointer
        transition-colors
        ${isDragActive ? 'border-primary bg-primary/5' : 'border-border'}
        ${isUploading ? 'opacity-50 cursor-not-allowed' : 'hover:border-primary'}
      `}
    >
      <input {...getInputProps()} />
      <div className="space-y-4">
        <div className="text-4xl">📄</div>
        {isUploading ? (
          <p>업로드 중...</p>
        ) : isDragActive ? (
          <p>파일을 놓아주세요</p>
        ) : (
          <>
            <p className="text-lg font-medium">
              PDF 파일을 드래그하거나 클릭하여 업로드하세요
            </p>
            <p className="text-sm text-muted-foreground">
              이력서, 경력기술서, 포트폴리오 등 (여러 파일 선택 가능)
            </p>
            {selectedFiles.length > 0 && (
              <div className="mt-4 space-y-2">
                <p className="text-sm font-medium">선택된 파일 ({selectedFiles.length}개):</p>
                <ul className="text-sm text-muted-foreground">
                  {selectedFiles.map((file, index) => (
                    <li key={index}>• {file.name}</li>
                  ))}
                </ul>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  )
}
