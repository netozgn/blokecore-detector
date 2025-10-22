from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader
import torch
from torch import nn, optim

# Transformações nas imagens
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# Carregar dataset
dataset = datasets.ImageFolder('dataset', transform=transform)
dataloader = DataLoader(dataset, batch_size=8, shuffle=True)

# Modelo base (pré-treinado)
model = models.mobilenet_v3_small(weights=models.MobileNet_V3_Small_Weights.DEFAULT)
model.classifier[3] = nn.Linear(model.classifier[3].in_features, len(dataset.classes))

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Treinamento simples
for epoch in range(5):  # pode aumentar se tiver mais dados
    total_loss = 0
    for imgs, labels in dataloader:
        optimizer.zero_grad()
        outputs = model(imgs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    print(f"Epoch {epoch+1} | Loss: {total_loss/len(dataloader):.4f}")

# Salvar modelo
torch.save({
    'model_state': model.state_dict(),
    'classes': dataset.classes
}, 'modelo_camisas.pth')

print("✅ Modelo treinado e salvo!")
