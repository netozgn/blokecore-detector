import cv2
import torch
from torchvision import transforms, models
from PIL import Image

# Carregar modelo
checkpoint = torch.load('modelo_camisas.pth', map_location='cpu')
classes = checkpoint['classes']

model = models.mobilenet_v3_small(weights=models.MobileNet_V3_Small_Weights.DEFAULT)
model.classifier[3] = torch.nn.Linear(model.classifier[3].in_features, len(classes))
model.load_state_dict(checkpoint['model_state'])
model.eval()

# Transformação de imagem
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

cap = cv2.VideoCapture(0)
print("Pressione Q para sair")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Recorta região central do frame (onde normalmente fica o tronco)
    h, w, _ = frame.shape
    roi = frame[int(h*0.3):int(h*0.8), int(w*0.3):int(w*0.7)]

    # Converte pra tensor
    img = Image.fromarray(cv2.cvtColor(roi, cv2.COLOR_BGR2RGB))
    img_t = transform(img).unsqueeze(0)

    # Predição
    with torch.no_grad():
        pred = model(img_t)
        label = classes[pred.argmax(1).item()]

    # Mostrar resultado
    cv2.putText(frame, f"Time: {label}", (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Reconhecimento de Camisa", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
