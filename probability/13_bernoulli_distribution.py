# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "marimo",
#     "matplotlib==3.10.0",
#     "numpy==2.2.3",
#     "scipy==1.15.2",
# ]
# ///

import marimo

__generated_with = "0.12.6"
app = marimo.App(width="medium", app_title="Bernoulli Distribution")


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Bernoulli Distribution

        > _Note:_ This notebook builds on concepts from ["Probability for Computer Scientists"](https://chrispiech.github.io/probabilityForComputerScientists/en/part2/bernoulli/) by Chris Piech.

        ## Parametric Random Variables

        Probability has a bunch of classic random variable patterns that show up over and over. Let's explore some of the most important parametric discrete distributions.

        Bernoulli is honestly the simplest distribution you'll ever see, but it's ridiculously powerful in practice. What makes it fascinating to me is how it captures any yes/no scenario: success/failure, heads/tails, 1/0.

        I think of these distributions as the atoms of probability — they're the fundamental building blocks that everything else is made from.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Bernoulli Random Variables

        A Bernoulli random variable boils down to just two possible values: 1 (success) or 0 (failure). dead simple, but incredibly useful.

        Some everyday examples where I see these:

        - Coin flip (heads=1, tails=0)
        - Whether that sketchy email is spam  
        - If someone actually clicks my ad
        - Whether my code compiles first try (almost always 0 for me)

        All you need (the classic expression) is a single parameter $p$ - the probability of success.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Key Properties of a Bernoulli Random Variable

        If $X$ is declared to be a Bernoulli random variable with parameter $p$, denoted $X \sim \text{Bern}(p)$, it has the following properties:
        """
    )
    return


@app.cell
def _(stats):
    # Define the Bernoulli distribution function
    def Bern(p):
        return stats.bernoulli(p)
    return (Bern,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Bernoulli Distribution Properties

        $\begin{array}{lll}
        \text{Notation:} & X \sim \text{Bern}(p) \\
        \text{Description:} & \text{A boolean variable that is 1 with probability } p \\
        \text{Parameters:} & p, \text{ the probability that } X = 1 \\
        \text{Support:} & x \text{ is either 0 or 1} \\
        \text{PMF equation:} & P(X = x) = 
            \begin{cases}
                p & \text{if }x = 1\\
                1-p & \text{if }x = 0
            \end{cases} \\
        \text{PMF (smooth):} & P(X = x) = p^x(1-p)^{1-x} \\
        \text{Expectation:} & E[X] = p \\
        \text{Variance:} & \text{Var}(X) = p(1-p) \\
        \end{array}$
        """
    )
    return


@app.cell(hide_code=True)
def _(mo, p_slider):
    # Visualization of the Bernoulli PMF
    _p = p_slider.value

    # Values for PMF
    values = [0, 1]
    probabilities = [1 - _p, _p]

    # Relevant statistics
    expected_value = _p
    variance = _p * (1 - _p)

    mo.md(f"""
    ## PMF Graph for Bernoulli($p={_p:.2f}$)

    Parameter $p$: {p_slider}

    Expected value: $E[X] = {expected_value:.2f}$

    Variance: $\\text{{Var}}(X) = {variance:.2f}$
    """)
    return expected_value, probabilities, values, variance


@app.cell(hide_code=True)
def _(expected_value, p_slider, plt, probabilities, values, variance):
    # PMF
    _p = p_slider.value
    fig, ax = plt.subplots(figsize=(10, 6))

    # Bar plot for PMF
    ax.bar(values, probabilities, width=0.4, color='blue', alpha=0.7)

    ax.set_xlabel('Values that X can take on')
    ax.set_ylabel('Probability')
    ax.set_title(f'PMF of Bernoulli Distribution with p = {_p:.2f}')

    # x-axis limit
    ax.set_xticks([0, 1])
    ax.set_xlim(-0.5, 1.5)

    # y-axis w/ some padding
    ax.set_ylim(0, max(probabilities) * 1.1)

    # Add expectation as vertical line
    ax.axvline(x=expected_value, color='red', linestyle='--', 
               label=f'E[X] = {expected_value:.2f}')

    # Add variance annotation
    ax.text(0.5, max(probabilities) * 0.8, 
            f'Var(X) = {variance:.3f}', 
            horizontalalignment='center',
            bbox=dict(facecolor='white', alpha=0.7))

    ax.legend()
    plt.tight_layout()
    plt.gca()
    return ax, fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Expectation and Variance of a Bernoulli

        > _Note:_ The following derivations are included as reference material. The credit for these mathematical formulations belongs to ["Probability for Computer Scientists"](https://chrispiech.github.io/probabilityForComputerScientists/en/part2/bernoulli/) by Chris Piech.

        Let's work through why $E[X] = p$ for a Bernoulli:

        \begin{align}
        E[X] &= \sum_x x \cdot (X=x) && \text{Definition of expectation} \\
        &= 1 \cdot p + 0 \cdot (1-p) &&
        X \text{ can take on values 0 and 1} \\
        &= p && \text{Remove the 0 term}
        \end{align}

        And for variance, we first need $E[X^2]$:

        \begin{align}
        E[X^2]
        &= \sum_x x^2 \cdot (X=x) &&\text{LOTUS}\\
        &= 0^2 \cdot (1-p) + 1^2 \cdot p\\
        &= p
        \end{align}

        \begin{align}
        (X)
        &= E[X^2] - E[X]^2&& \text{Def of variance} \\
        &= p - p^2 && \text{Substitute }E[X^2]=p, E[X] = p \\
        &= p (1-p) && \text{Factor out }p
        \end{align}
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Indicator Random Variables

        Indicator variables are a clever trick I like to use — they turn events into numbers. Instead of dealing with "did the event happen?" (yes/no), we get "1" if it happened and "0" if it didn't.

        Formally: an indicator variable $I$ for event $A$ equals 1 when $A$ occurs and 0 otherwise. These are just bernoulli variables where $p = P(A)$. people often use notation like $I_A$ to name them.

        Two key properties that make them super useful:

        - $P(I=1)=P(A)$ - probability of getting a 1 is just the probability of the event
        - $E[I]=P(A)$ - the expected value equals the probability (this one's a game-changer!)
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    # Simulation of Bernoulli trials
    mo.md(r"""
    ## Simulation of Bernoulli Trials

    Let's simulate Bernoulli trials to see the law of large numbers in action. We'll flip a biased coin repeatedly and observe how the proportion of successes approaches the true probability $p$.
    """)

    # UI element for simulation parameters
    num_trials_slider = mo.ui.slider(10, 10000, value=1000, step=10, label="Number of trials")
    p_sim_slider = mo.ui.slider(0.01, 0.99, value=0.65, step=0.01, label="Success probability (p)")
    return num_trials_slider, p_sim_slider


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Simulation""")
    return


@app.cell(hide_code=True)
def _(mo, num_trials_slider, p_sim_slider):
    mo.hstack([num_trials_slider, p_sim_slider], justify='space-around')
    return


@app.cell(hide_code=True)
def _(np, num_trials_slider, p_sim_slider, plt):
    # Bernoulli trials
    _num_trials = num_trials_slider.value
    p = p_sim_slider.value

    # Random Bernoulli trials
    trials = np.random.binomial(1, p, size=_num_trials)

    # Cumulative proportion of successes
    cumulative_mean = np.cumsum(trials) / np.arange(1, _num_trials + 1)

    # Results
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, _num_trials + 1), cumulative_mean, label='Proportion of successes')
    plt.axhline(y=p, color='r', linestyle='--', label=f'True probability (p={p})')

    plt.xscale('log')  # Use log scale for better visualization
    plt.xlabel('Number of trials')
    plt.ylabel('Proportion of successes')
    plt.title('Convergence of Sample Proportion to True Probability')
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Add annotation
    plt.annotate('As the number of trials increases,\nthe proportion approaches p',
                xy=(_num_trials, cumulative_mean[-1]), 
                xytext=(_num_trials/5, p + 0.1),
                arrowprops=dict(facecolor='black', shrink=0.05, width=1))

    plt.tight_layout()
    plt.gca()
    return cumulative_mean, p, trials


@app.cell(hide_code=True)
def _(mo, np, trials):
    # Calculate statistics from the simulation
    num_successes = np.sum(trials)
    num_trials = len(trials)
    proportion = num_successes / num_trials

    # Display the results
    mo.md(f"""
    ### Simulation Results

    - Number of trials: {num_trials}
    - Number of successes: {num_successes}
    - Proportion of successes: {proportion:.4f}

    This demonstrates how the sample proportion approaches the true probability $p$ as the number of trials increases.
    """)
    return num_successes, num_trials, proportion


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## 🤔 Test Your Understanding

        Pick which of these statements about Bernoulli random variables you think are correct:

        /// details | The variance of a Bernoulli random variable is always less than or equal to 0.25
        ✅ Correct! The variance $p(1-p)$ reaches its maximum value of 0.25 when $p = 0.5$.
        ///

        /// details | The expected value of a Bernoulli random variable must be either 0 or 1
        ❌ Incorrect! The expected value is $p$, which can be any value between 0 and 1.
        ///

        /// details | If $X \sim \text{Bern}(0.3)$ and $Y \sim \text{Bern}(0.7)$, then $X$ and $Y$ have the same variance
        ✅ Correct! $\text{Var}(X) = 0.3 \times 0.7 = 0.21$ and $\text{Var}(Y) = 0.7 \times 0.3 = 0.21$.
        ///

        /// details | Two independent coin flips can be modeled as the sum of two Bernoulli random variables
        ✅ Correct! The sum would follow a Binomial distribution with $n=2$.
        ///
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Applications of Bernoulli Random Variables

        Bernoulli random variables are used in many real-world scenarios:

        1. **Quality Control**: Testing if a manufactured item is defective (1) or not (0)

        2. **A/B Testing**: Determining if a user clicks (1) or doesn't click (0) on a website button

        3. **Medical Testing**: Checking if a patient tests positive (1) or negative (0) for a disease

        4. **Election Modeling**: Modeling if a particular voter votes for candidate A (1) or not (0)

        5. **Financial Markets**: Modeling if a stock price goes up (1) or down (0) in a simplified model

        Because Bernoulli random variables are parametric, as soon as you declare a random variable to be of type Bernoulli, you automatically know all of its pre-derived properties!
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Summary

        And that's a wrap on Bernoulli distributions! We've learnt the simplest of all probability distributions — the one that only has two possible outcomes. Flip a coin, check if an email is spam, see if your blind date shows up — these are all Bernoulli trials with success probability $p$. 

        The beauty of Bernoulli is in its simplicity: just set $p$ (the probability of success) and you're good to go! The PMF gives us $P(X=1) = p$ and $P(X=0) = 1-p$, while expectation is simply $p$ and variance is $p(1-p)$. Oh, and when you're tracking whether specific events happen or not? That's an indicator random variable — just another Bernoulli in disguise!

        Two key things to remember:

        /// note
        💡 **Maximum Variance**: A Bernoulli's variance $p(1-p)$ reaches its maximum at $p=0.5$, making a fair coin the most "unpredictable" Bernoulli random variable.

        💡 **Instant Properties**: When you identify a random variable as Bernoulli, you instantly know all its properties—expectation, variance, PMF—without additional calculations.
        ///

        Next up: Binomial distribution—where we'll see what happens when we let Bernoulli trials have a party and add themselves together!
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""#### Appendix (containing helper code for the notebook)""")
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _():
    from marimo import Html
    return (Html,)


@app.cell(hide_code=True)
def _():
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy import stats
    import math

    # Set style for consistent visualizations
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.rcParams['figure.figsize'] = [10, 6]
    plt.rcParams['font.size'] = 12

    # Set random seed for reproducibility
    np.random.seed(42)
    return math, np, plt, stats


@app.cell(hide_code=True)
def _(mo):
    # Create a UI element for the parameter p
    p_slider = mo.ui.slider(0.01, 0.99, value=0.65, step=0.01, label="Parameter p")
    return (p_slider,)


if __name__ == "__main__":
    app.run()
