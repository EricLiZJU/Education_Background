import torch
print(torch.backends.mps.is_available())     # True → 说明系统支持 MPS
print(torch.backends.mps.is_built())         # True → 说明 PyTorch 支持 MPS