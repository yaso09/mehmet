name: Bug bildirimi

description: Bir hata veya beklenmeyen davranış bildir

title: "[Bug] "
labels: [bug]

body:
  - type: textarea
    id: what
    attributes:
      label: Ne oldu?
      description: Beklenen ve gerçekleşen davranışı açıkla
    validations:
      required: true

  - type: textarea
    id: repro
    attributes:
      label: Tekrarlama adımları
      description: Sorunu tekrarlamak için adımlar
    validations:
      required: false