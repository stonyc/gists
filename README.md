Various scripts and short pipelines that may be useful.

**NOTE**: most snippets assume Ubuntu v18.04+

TEMP:

Adding `predict_step` to Transformer model:

```python
    def predict_step(self, batch, batch_idx, dataloader_idx=0):
        x, y = batch
        return self(x)
```

Then predict using trained model:

```python
preds = trainer.predict(model, <data_loader>)
```
