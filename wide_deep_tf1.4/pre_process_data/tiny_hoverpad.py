#coding=utf-8
import luigi
import collections

class RawMetaData(luigi.ExternalTask):
    def output(self):
        return luigi.LocalTarget('../../data/meta_Books.json')

class ItemInfo(luigi.Task):
    n = luigi.IntParameter(default=10)
    def requires(self):
        return RawMetaData()

    def output(self):
        return luigi.LocalTarget('item_info.data')

    def run(self):
        with self.input().open('r') as f_in, self.output().open('w') as f_out:
            for line in f_in:
                obj = eval(line)
                cat = obj['categories'][0][-1]
                print >> f_out, obj['asin'] + '\t' + cat
        #end-with

class RawReviewData(luigi.ExternalTask):
    def output(self):
        return luigi.LocalTarget('../../data/review_Books.json')

class ReviewInfo(luigi.Task):
    def requires(self):
        return RawReviewData()

    def output(self):
        return luigi.LocalTarget('review_info.data')

    def run(self):
        user_map = {}
        with self.input().open('r') as f_in, self.output().open('w') as f_out:
            for line in f_in:
                obj = eval(line)
                userID = obj["reviewerID"]
                itemID = obj["asin"]
                rating = obj["overall"]
                time = obj["unixReviewTime"]
                print>>fo, userID + "\t" + itemID + "\t" + str(rating) + "\t" + str(time)
        #end-with

class OnlineJoiner(luigi.Task):
    n = luigi.IntParameter(default=10)
    def requires(self):
        return [ItemInfo(), ReviewInfo()]

    def output(self):
        return luigi.LocalTarget('jointed_new.data')

    def run(self):
        user_map = collections.default(list)
        item_map = collections.default(list)
        item_list = []
        with self.input()[0].open('r') as fin_item, self.input()[1].open('r') as fin_rev \
            self.output().open('w') as fout:
            for line in fin_rev:
                items = line.strip().split("\t")
                user_map[items[0]].append(("\t").join(items), float(items[-1])))
                item_list.append(items[1])

            for line in fin_item:
                arr = line.strip().split("\t")
                item_map[arr[0]] = arr[1]

            for key in user_map:
                sorted_user_bh = sorted(user_map[key], key=lambda x:x[1])
                for line,t in sorted_user_bh:
                    items = line.split("\t")
                    asin = items[1]
        #end-with

if __name__ == '__main__':
    luigi.run()

