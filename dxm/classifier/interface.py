from exceptions import NotImplementedError
import abc

class MultinomialBayesClassifier(object):
    """Defines a multinomial bayes classifier. This classifier can be be trained
    multiple times via the train function. Use predict to make new predictions
    on inputs. 
    """
    def __init__(self, extractor=None, common=None):
        """Tokens as a word -> index dict. Labels as label -> index dict"""
        if extractor == None or common == None: raise UnboundLocalError
        self.update_common(common)
        self.extractor = extractor
        self.num_tokens = self.d.num_tokens
        self.num_labels = self.d.num_labels  
        self.counts_y = np.zeros((self.d.num_labels, 1))
        self.m = np.uint32(0)
        self.counts = lil_matrix((self.d.num_labels, self.d.num_tokens))
        self.totals = lil_matrix((self.d.num_tokens, 1))
        self.modified = 1    
        self.statuses = set()
        
    def update_common(self, common):
        setattr(self, 'd', common)
        
    def train(self, sr_tup):
        """Train a classifer with (status, rating) tuple, can be trained more"""
        d = self.d
        self.modified += 1
        status = sr_tup[0]
        if status.id in self.statuses or not status.text: return
        self.statuses.add(sr_tup[0].id)
        feats = [(t, sr_tup[1]) for t in self.extractor.ExtractStatus(sr_tup[0])]
        for token, label in feats:
            i = d.labels[label]
            try: j = d.tokens[token]
            except KeyError: continue
            self.counts[i, j] += 1
            self.totals[j, 0] += 1
            self.counts_y[i, 0] += 1
            self.m += 1
        
            
    def _freeze(self):
        """Freeze the classifier in a state to increase performance"""
        self.log_phi_y = np.log(self.counts_y/self.m)
        self.log_phi_x_y = csc_matrix(np.log(np.divide(
                         self.counts.todense() + 1, 
                         np.transpose(self.totals.todense()) + self.num_tokens)))
        self.modified = 0            
            
    def predict(self, status):
        """Predict status using the classifier, returns list"""
        return NotImplementedError
