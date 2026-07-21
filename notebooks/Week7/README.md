This week I chose Gradient Boosting over a Random Forest and a small neural network for our
ED triage model — here's why, in one paragraph: neither the Random Forest nor the neural
network actually beat our simple logistic regression baseline on overall performance, which
was the more surprising result of the week. Gradient Boosting was the exception — it improved
recall on the most critical patient group (ESI 1) from 25% to 31%, the one number we'd already
agreed mattered most clinically, even though it scored lower on accuracy and is harder to
explain than the other models. The lesson: more complexity doesn't automatically buy you
anything, and it's worth benchmarking honestly against your simplest baseline before assuming
otherwise.
