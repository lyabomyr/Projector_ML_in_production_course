import hydra
from omegaconf import DictConfig, OmegaConf

@hydra.main(version_base=None, config_path="conf", config_name="correct_train_parametrs")
def generate_model_card(cfg: OmegaConf):

	print(f"Batch size is {cfg.param.max_depth}")

generate_model_card()