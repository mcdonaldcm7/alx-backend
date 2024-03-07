import express from 'express';
import { createClient } from 'redis';
import util from 'util';

const listProducts = [
  { itemId: 1, itemName: 'Suitcase 250', price: 50, initialAvailableQuantity: 4 },
  { itemId: 2, itemName: 'Suitcase 450', price: 100, initialAvailableQuantity: 10 },
  { itemId: 3, itemName: 'Suitcase 650', price: 350, initialAvailableQuantity: 2 },
  { itemId: 4, itemName: 'Suitcase 1050', price: 550, initialAvailableQuantity: 5 }
];

function getItemById (id) {
  for (const item of listProducts) {
    if (item.itemId === Number(id)) {
      return item;
    }
  }
}

const app = express();
const port = 1245;

const client = createClient();

app.get('/list_products', (req, res) => {
  const availableProduct = [];
  for (const item in listProducts) {
    const qty = listProducts[item].currentQuantity;
    if ((qty === undefined || qty > 0) && listProducts[item].initialAvailableQuantity > 0) {
      availableProduct.push(listProducts[item]);
    }
  }
  res.status(200).json(availableProduct);
});

async function reserveStockById (itemId, stock) {
  for (const item of listProducts) {
    if (item.itemId === Number(itemId)) {
      return await client.incrby(`item.${itemId}`, stock);
    }
  }
}

const clientGet = util.promisify(client.get).bind(client);

const getCurrentReservedStockById = async (itemId) => {
  return await clientGet(`item.${itemId}`);
};

app.get('/list_products/:itemId', (req, res) => {
  const id = req.params.itemId;
  getCurrentReservedStockById(id)
    .then((result) => {
      const itemInfo = getItemById(id);

      if (itemInfo === undefined) {
        res.status(500).json({ status: 'Product not found' });
        return;
      }

      itemInfo.currentQuantity = itemInfo.initialAvailableQuantity - result;
      res.status(200).json(itemInfo);
    });
});

app.get('/reserve_product/:itemId', (req, res) => {
  const id = req.params.itemId;
  const item = getItemById(id);

  getCurrentReservedStockById(id)
    .then((result) => {
      if (item === undefined) {
        res.status(500).json({ status: 'Product not found' });
        return;
      }
      if (Number(result) >= item.initialAvailableQuantity) {
        res.status(500).json({ status: 'Not enough stock available', itemId: id });
        return;
      }
      reserveStockById(id, 1)
        .then((stocked) => {
          if (stocked) {
            res.status(200).json({ status: 'Reservation confirmed', itemId: id });
          } else {
            res.status(500).json({ status: 'Product not found' });
          }
        });
    });
});

app.listen(port, () => {
  console.log('...');
});
