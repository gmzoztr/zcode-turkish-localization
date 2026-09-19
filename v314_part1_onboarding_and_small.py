# -*- coding: utf-8 -*-
"""
v314_part1_onboarding_and_small.py
occupationOnboarding (43 keys) + small prefixes (76 keys) translations
"""

PART1_TR = {
    # occupationOnboarding
    "occupationOnboarding.stepRole": "Çalışma Alanınız",
    "occupationOnboarding.stepMode": "Arayüz modu",
    "occupationOnboarding.modeTitle": "Arayüz modunuzu seçin",
    "occupationOnboarding.modeDescription": "ZCode'un çalışmasını nasıl göstermesini istersiniz?",
    "occupationOnboarding.coding": "Kodlama modu",
    "occupationOnboarding.codingDescription": "Geliştirme süreci boyunca kodu, komut çıktılarını ve değişiklik ayrıntılarını görmek istiyorum.",
    "occupationOnboarding.officeMode": "Ofis modu",
    "occupationOnboarding.officeModeDescription": "Kod, komut çıktısı veya diğer teknik ayrıntılara gerek duymadan görev ilerlemesine ve sonuçlara odaklanırım.",
    "occupationOnboarding.suggestionsHeading": "Önerilen görevler",
    "occupationOnboarding.infrastructure": "QA / Operasyon / Güvenlik",
    "occupationOnboarding.product": "Ürün / Proje / Çözümler",
    "occupationOnboarding.design": "UI / UX / Görsel Tasarım",
    "occupationOnboarding.creator": "Medya / İçerik Üretimi",
    "occupationOnboarding.operations": "Operasyon / Ticaret / Müşteri Hizmetleri",
    "occupationOnboarding.marketing": "Pazarlama / Marka / PR",
    "occupationOnboarding.finance": "Finans / Muhasebe / Danışmanlık",
    "occupationOnboarding.independent": "Girişimcilik / Serbest Çalışan (Freelance) / Tek Kişilik Şirket",
    "occupationOnboarding.accounting": "Muhasebe / Denetim / Vergi",
    "occupationOnboarding.legal": "Hukuk / İdari İşler / İK",
    "occupationOnboarding.skip": "Atla",
    "occupationOnboarding.start": "Başlayın",
    "occupationOnboarding.continue": "İleri",
    "occupationOnboarding.saving": "Kaydediliyor…",
    "occupationOnboarding.back": "Geri",
    "occupationOnboarding.error": "Kaydedilemedi. Lütfen tekrar deneyin.",
    "occupationOnboarding.stepPreferences": "Tercihler",
    "occupationOnboarding.heroTitle": "Basit, Hızlı, İlham Dolu!",
    "occupationOnboarding.heroDescription": "Çoklu ajanlarla karmaşık hedefleri gerçekleştirin.\nNerede olursanız olun kontrolü elinizde tutun.",
    "occupationOnboarding.title": "Ne ile ilgileniyorsunuz?",
    "occupationOnboarding.description": "Günlük işinize en yakın seçeneği belirleyin.",
    "occupationOnboarding.office": "Ofis çalışanı",
    "occupationOnboarding.developer": "Yazılım / Veri / Yapay Zeka",
    "occupationOnboarding.student": "Öğrenci / Eğitim / Araştırma",
    "occupationOnboarding.other": "Diğer meslekler",
    "occupationOnboarding.preferences": "Çalışma asistanınızı kişiselleştirin",
    "occupationOnboarding.preferencesDescription": "Hangi özelliklerin etkinleştirileceğini seçin.",
    "occupationOnboarding.migration": "Sohbetleri içe aktar",
    "occupationOnboarding.migrationDescription": "Claude Code'daki sohbet geçmişini içe aktarın",
    "occupationOnboarding.memory": "Çalışma Alanı Belleğini Etkinleştir",
    "occupationOnboarding.memoryDescription": "ZCode'un tercihlerinizi ve çalışma bağlamınızı hatırlamasına izin verin.",
    "occupationOnboarding.suggestions": "Proaktif görev önerilerini etkinleştir",
    "occupationOnboarding.suggestionsDescription": "Yeni sohbetlerde önerileri göster. Düzenleyiciye eklemek için tıklayın.",
    "occupationOnboarding.close": "Rehberden çık",

    # startPlan
    "startPlan.recommendation.subagentDescription": "Başlangıç Planınızda {model} için kullanılabilir kota bulunuyor. Bu alt ajanın modelini Başlangıç Planına geçirmek ister misiniz?",
    "startPlan.recommendation.preferenceSaveFailed": "“Bir daha sorma” kaydedilemedi. Bu işlem için seçiminizle devam ediliyor.",
    "startPlan.recommendation.title": "Başlangıç Planı kotası mevcut",
    "startPlan.recommendation.description": "Başlangıç Planınızda hâlâ {model} için kota bulunuyor. Kullanmak ister misiniz?",
    "startPlan.recommendation.switch": "Planı değiştir",
    "startPlan.recommendation.decline": "Şimdi değil",
    "startPlan.recommendation.dismiss": "Bir daha gösterme",

    # marketingTouch
    "marketingTouch.idle": "Hazır",
    "marketingTouch.verifying": "Doğrulanıyor…",
    "marketingTouch.submitting": "İşleniyor…",
    "marketingTouch.preparing": "Başarılı. Sonuç hazırlanıyor…",
    "marketingTouch.failed": "İşlem başarısız oldu. Lütfen daha sonra tekrar deneyin.",
    "marketingTouch.uncertain": "Sonuç doğrulanamadı. Avantajlarınızı daha sonra kontrol edin. Mükerrer gönderimleri önlemek için bu işlem bu oturumda tekrar denenmeyecektir.",
    "marketingTouch.succeeded": "İşlem başarılı",

    # rewards
    "rewards.title": "Ödüller",
    "rewards.menuTitle": "Arkadaşını Davet Et",
    "rewards.menuBadge": "Ödüller",
    "rewards.loadFailed": "Bu sayfa yüklenemedi. Lütfen tekrar deneyin.",
    "rewards.openWebsite": "Web sitesini aç",

    # sidePane
    "sidePane.workflowRun": "İş akışı çalıştırması",
    "sidePane.workflowDirectory": "İş akışı çalıştırmaları",
    "sidePane.workflowActor": "İş akışı alt ajanı",
    "sidePane.workflowScript": "Komut dosyası adımları",
    "sidePane.workflowArtifact": "Çıktı / Yapay Nesne",

    # pluginCreator
    "pluginCreator.add": "Ekle",
    "pluginCreator.create": "Eklenti oluştur",
    "pluginCreator.addMarketplace": "Eklenti mağazası ekle",
    "pluginCreator.unavailable": "Eklenti Oluşturucu kullanılamıyor. Bağlantıyı kontrol edin, ardından mağazada Eklenti Oluşturucu'yu etkinleştirip veya geri yükleyip tekrar deneyin.",

    # automations
    "automations.pageTab.ariaLabel": "Otomasyonlar sayfası",
    "automations.pageTab.automation": "Otomasyonlar",
    "automations.pageTab.workflow": "İş Akışları",

    # tokenDebug
    "tokenDebug.column.tps": "TPS (token/sn)",
    "tokenDebug.tpsDescription": "Çıktı tokenleri ÷ ilk çıktı tokeninden istek tamamlanmasına kadar geçen saniye",

    # zcode
    "zcode.error.MEDIA_BUDGET_CURRENT_ATTACHMENT_TOO_LARGE": "Mevcut ekler tek bir istek için çok büyük. Ekleri kaldırın veya sıkıştırıp tekrar deneyin.",
    "zcode.error.providerBusiness.3102": "Bu çalıştırma maksimum tek çalıştırma süresini aştı. Devam etmek için yeni bir yoğun olmayan saat görevi oluşturun.",

    # desktopMenu
    "desktopMenu.help.restartUpdateAction": "Yeniden Başlat ve Güncelle",

    # developerTools
    "developerTools.loadError": "Hata ayıklama verileri okunamadı. Yeniden deneniyor; önceki kayıtlar güncel olmayabilir.",

    # feedback
    "feedback.submit.simple.screenshotPrivacyHint": "Lütfen yüklemeden önce görüntülerde özel bilgi olup olmadığını kontrol edin.",

    # taskList
    "taskList.deleteAllArchived": "Tüm arşivlenmiş görevleri sil",
    "taskList.archivedActions": "Arşiv işlemleri",
    "taskList.archivedTaskCount": "{count} arşivlenmiş görev",
    "taskList.deleteAllArchivedMenu": "Tüm arşivlenmiş görevleri sil…",
    "taskList.deleteAllArchivedTitle": "{count} arşivlenmiş görev silinsin mi?",
    "taskList.deleteAllArchivedBusy": "İşleniyor…",
    "taskList.deleteAllArchivedUnavailable": "Bu projeler şu anda işlenemiyor: {projects}. Yeniden bağlandıktan sonra tekrar deneyin.",
    "taskList.deleteAllArchivedResult": "{deleted} silindi, {skipped} atlandı, {failed} başarısız oldu.",
    "taskList.deleteAllArchivedError": "İşlem veya liste yenileme başarısız oldu. Kalan görevleri kontrol etmek için yenileyin.",
    "taskList.workflowRun.ariaLabel": "İş akışı çalıştırması {name}: {status}",
    "taskList.workflowRun.moreRuns": "+{count} daha",
    "taskList.workflowRun.moreStations": "+{count}",
    "taskList.workflowRun.liveCount": "{count} iş akışı çalışıyor",

    # bashOutput
    "bashOutput.open": "{title} için çıktıyı görüntüle",
    "bashOutput.fullFile": "Tam çıktı dosyası",
    "bashOutput.retry": "Tekrar Dene",
    "bashOutput.empty": "Henüz çıktı yok",
    "bashOutput.status.running": "Çalışıyor",
    "bashOutput.error.unavailable": "Görev veya oturum kullanılamıyor",
    "bashOutput.error.unsupported": "Bu çalışma zamanı arka plan çıktısını desteklemiyor",
    "bashOutput.error.read_failed": "Çıktı dosyası okunamadı",
    "bashOutput.error.query_failed": "Görev çalışma zamanına bağlanılamadı",

    # workflowDirectory
    "workflowDirectory.title": "İş akışı çalıştırmaları",
    "workflowDirectory.running": "Çalışıyor",
    "workflowDirectory.runningEmpty": "Çalışan iş akışı yok",
    "workflowDirectory.ended": "Sona Erdi",
    "workflowDirectory.endedEmpty": "Henüz sona eren iş akışı yok",
    "workflowDirectory.empty": "Bu sohbette henüz bir iş akışı çalıştırılmadı",
    "workflowDirectory.truncated": "Yalnızca en son {count} çalıştırma gösteriliyor",
    "workflowDirectory.unavailable": "Bu sohbet için iş akışı çalıştırmaları listelenemiyor",
}
