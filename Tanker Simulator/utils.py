import matplotlib.pyplot as plt


def plot_hist(psi, refs, rudder_hist):
    fig, axs = plt.subplots(2, 1)

    axs[0].plot(psi, color="black", linewidth=1, label="Ship heading")
    axs[0].plot(refs, color="black", linewidth=1, linestyle="--", label="Desired ship heading")
    axs[0].set_title('Ship heading vs Desired ship heading')
    axs[0].legend()
    axs[0].set(ylabel='[deg]')
    axs[0].grid(True)

    axs[1].plot(rudder_hist, color="black", linewidth=1, label="Ship heading")
    axs[1].set_title('Rudder Angle')
    axs[1].set(xlabel='time [s]', ylabel=f'$\delta$ [deg]')
    axs[1].grid(True)

    fig.tight_layout()
    plt.show()