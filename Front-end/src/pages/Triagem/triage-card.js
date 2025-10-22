export function calculateBMI(weight, height) {
    return Number((weight / (height * height)).toFixed(1))
  }
  
  export function getBMICategory(bmi) {
    if (bmi < 18.5) return "Abaixo do peso"
    if (bmi < 25) return "Peso normal"
    if (bmi < 30) return "Sobrepeso"
    return "Obesidade"
  }
  
  export function formatDateTime(dateString) {
    const date = new Date(dateString)
    return date.toLocaleString("pt-BR", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    })
  }
  