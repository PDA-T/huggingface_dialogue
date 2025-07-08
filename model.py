from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import os


class ChatModel:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.cache_dir = "./my_models"

    def load_model(self, model_name):
        # 检查模型是否已下载
        local_path = os.path.join(self.cache_dir, model_name.replace("/", "_"))
        if os.path.exists(local_path):
            self.tokenizer = AutoTokenizer.from_pretrained(local_path)
            self.model = AutoModelForCausalLM.from_pretrained(local_path)
            self.model.to(self.device)
            return "模型已存在，装载成功"
        else:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=self.cache_dir)
            self.model = AutoModelForCausalLM.from_pretrained(model_name, cache_dir=self.cache_dir)
            self.model.save_pretrained(local_path)
            self.tokenizer.save_pretrained(local_path)
            self.model.to(self.device)
            return "模型下载并装载成功"

    def chat(self, user_input):
        if self.model is None or self.tokenizer is None:
            return "请先加载模型"
        prompt = f"用户：{user_input}\n助手："
        inputs = self.tokenizer(prompt, return_tensors="pt")
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        outputs = self.model.generate(**inputs, max_new_tokens=100, pad_token_id=self.tokenizer.eos_token_id)
        reply = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        answer = reply[len(prompt):].strip().split("用户：")[0].strip()
        return answer
