name: Özellik isteği

description: Yeni bir özellik veya iyileştirme öner

title: "[Özellik] "
labels: [enhancement]

body:
  - type: textarea
    id: motivation
    attributes:
      label: Motivasyon
      description: Bu özellik neden gerekli?
    validations:
      required: true

  - type: textarea
    id: proposal
    attributes:
      label: Öneri
      description: Nasıl uygulanabilir?
    validations:
      required: false