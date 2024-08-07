
;; Added by Package.el.  This must come before configurations of
;; installed packages.  Don't delete this line.  If you don't want it,
;; just comment it out by adding a semicolon to the start of the line.
;; You may delete these explanatory comments.
(require 'package)
(setq package-archives
    '(("melpa" . "http://melpa.org/packages/")
      ("melpa-stable" . "http://stable.melpa.org/packages/")))
(package-initialize)

(custom-set-variables
 ;; custom-set-variables was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(cua-mode t nil (cua-base))
 '(package-selected-packages '(flycheck flymake swiper counsel ivy web-mode company)))
(custom-set-faces
 ;; custom-set-faces was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 )

(global-set-key (kbd "<zenkaku-hankaku>") 'toggle-input-method)

(add-hook 'mozc-mode-hook
  (lambda()
    (define-key mozc-mode-map (kbd "<zenkaku-hankaku>") 'toggle-input-method)))

;;line number
(global-linum-mode t)
(setq linum-format "%d ")

;;MOZC
(require 'mozc)

(set-language-environment "Japanese")

(setq default-input-method "japanese-mozc")

(setq make-backup-files nil)

(setq auto-save-default nil)

(prefer-coding-system 'utf-8)
(setq coding-system-for-read 'utf-8)
(setq coding-system-for-write 'utf-8)

(electric-indent-mode -1)

;;company
(global-company-mode t)
(global-set-key (kbd "C-f") 'company-complete)

;;ivy
(ivy-mode 1)

;;
;; whitespace
;;
(require 'whitespace)
(setq whitespace-style '(face           ; faceで可視化
                         trailing       ; 行末
                         tabs           ; タブ
;;                         empty          ; 先頭/末尾の空行
                         space-mark     ; 表示のマッピング
                         tab-mark
                         ))

(setq whitespace-display-mappings
      '((tab-mark ?\t [?\u00BB ?\t] [?\\ ?\t])))

(global-whitespace-mode 1)

;;flycheck
(setq flycheck-check-syntax-automatically
  '(save idle-change mode-enabled))
