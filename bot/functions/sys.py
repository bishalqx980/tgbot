async def func_sys(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    power_users = await _power_users()
    if user.id not in power_users:
        await Message.reply_msg(update, "❗ This command is only for bot owner!")
        return
    
    sys_info = (
        f"<b>↺ System info</b>\n\n"
        f"• CPU\n"
        f"CPU: <code>{psutil.cpu_count()}</code>\n"
        f"CPU (Logical): <code>{psutil.cpu_count(False)}</code>\n"
        f"CPU freq Current: <code>{psutil.cpu_freq()[0]/1024:.2f} Ghz</code>\n"
        f"CPU freq Max: <code>{psutil.cpu_freq()[2]/1024:.2f} Ghz</code>\n\n"
        f"• RAM\n"
        f"RAM Total: <code>{psutil.virtual_memory()[0]/(1024**3):.2f} GB</code>\n"
        f"RAM Avail: <code>{psutil.virtual_memory()[1]/(1024**3):.2f} GB</code>\n"
        f"RAM Used: <code>{psutil.virtual_memory()[3]/(1024**3):.2f} GB</code>\n"
        f"RAM Free: <code>{psutil.virtual_memory()[4]/(1024**3):.2f} GB</code>\n"
        f"RAM Percent: <code>{psutil.virtual_memory()[2]} %</code>\n\n"
        f"• RAM (Swap)\n"
        f"RAM Total (Swap): <code>{psutil.swap_memory()[0]/(1024**3):.2f} GB</code>\n"
        f"RAM Used (Swap): <code>{psutil.swap_memory()[1]/(1024**3):.2f} GB</code>\n"
        f"RAM Free (Swap): <code>{psutil.swap_memory()[2]/(1024**3):.2f} GB</code>\n"
        f"RAM Percent (Swap): <code>{psutil.swap_memory()[3]} %</code>\n\n"
        f"• Drive/Storage\n"
        f"Total Partitions: <code>{len(psutil.disk_partitions())}</code>\n"
        f"Disk Usage Total: <code>{psutil.disk_usage('/')[0]/(1024**3):.2f} GB</code>\n"
        f"Disk Usage Used: <code>{psutil.disk_usage('/')[1]/(1024**3):.2f} GB</code>\n"
        f"Disk Usage Free: <code>{psutil.disk_usage('/')[2]/(1024**3):.2f} GB</code>\n"
        f"Disk Usage Percent: <code>{psutil.disk_usage('/')[3]} %</code>\n\n"
    )
    await Message.reply_msg(update, sys_info)