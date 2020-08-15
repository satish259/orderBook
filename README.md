# orderBook

A simple order book to process string messages received one by one.

## Usage

git pull --no-commit https://github.com/satish259/orderBook.git

or

[Download](https://github.com/satish259/orderBook/archive/master.zip)

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## History
2020-08-03 [Initial release](https://github.com/satish259/orderBook/commit/e799584601bf9d6e1365673225c8c6b63a4f1c88)

2020-08-11 [Updated implementation](https://github.com/satish259/orderBook/archive/master.zip)

## Future enhancments suggestions
1) If speed of getBestBidAndAsk becomes an issue due to length of list, a numpy array of dtype float (with numpy.max and numpy.min) could be used to make it faster.
2) Add permanent DB to store data for analytics. (Celery is used to make DB operations via async task queue).
3) Identify possible arbitrage scenarios based on quantity and priced.

## License

This project as available as open source.
