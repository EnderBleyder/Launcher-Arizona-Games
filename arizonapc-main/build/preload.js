(() => {
    var e = {
            4157: e => {
                "use strict";
                e.exports = require("electron")
            }
        },
        n = {};
    const {
        contextBridge: i,
        ipcRenderer: s
    } = function i(s) {
        var o = n[s];
        if (void 0 !== o) return o.exports;
        var t = n[s] = {
            exports: {}
        };
        return e[s](t, t.exports, i), t.exports
    }(4157);
    i.exposeInMainWorld("launcherAPI", {
        openUrlInBrowser: e => s.send("open-url", e),
        closeApp: () => s.send("close-app"),
        maximizeWindow: () => s.send("maximize-window"),
        minimizeWindow: () => s.send("minimize-window"),
        validateAndStartGame: (e, n, i, o, t, a, r) => s.send("validateAndStartGame", e, n, i, o, t, a, r),
        validateGameFiles: e => s.send("validateGameFiles", e),
        repairGameFiles: (e, n) => s.send("repairGameFiles", e, n),
        installDrivers: e => s.send("installDrivers", e),
        handleDriverInstallProgress: e => s.on("drivers:installProgress", e),
        handleProgress: e => s.on("progress-update", e),
        handleUpdateModalVisibility: e => s.on("update-modal-visibility", e),
        handleNetworkErrorModalVisibility: e => s.on("network-error-modal-visibility", e),
        handleAppVersionUpdate: e => s.on("update-app-version", e),
        getSettings: e => s.invoke("getSettings", e),
        setSettings: (e, n) => s.send("setSettings", e, n),
        exitLauncher: e => s.send("exitLauncher", e),
        selectDirectory: (e = "") => s.invoke("directory:select", e),
        openGameFolder: (e = "") => s.send("openGameFolder", e),
        restartAsAdmin: () => s.send("restartAsAdmin"),
        handleRestartAsAdminModalVisibility: e => s.on("restart-as-admin-modal-visibility", e),
        toggleAutoLaunch: e => s.send("toggleAutoLaunch", e),
        handleAutoLaunchModalVisibility: e => s.on("auto-launch-modal-visibility", e),
        handleUpdateDownloadInProgress: e => s.on("update-download-in-progress", e),
        handleUnknownErrorModalVisibility: e => s.on("unknown-error-modal-visibility", e),
        requestMods: e => s.send("mods:request", e),
        handleModsInitialize: e => s.on("mods:load", e),
        onModInstallChange: e => s.on("mod:onInstallChange", e),
        installMod: (e, n) => s.send("mod:install", e, n),
        uninstallMod: (e, n) => s.send("mod:uninstall", e, n)
    })
})();