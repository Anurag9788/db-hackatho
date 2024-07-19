document.addEventListener("DOMContentLoaded", function (event) {
    var r = document.querySelector(':root');

    switch (InstanceCode.toLowerCase()) {
        case 'development':
            r.style.setProperty('--color', '195, 107, 132');
            break;
        case 'working':
            r.style.setProperty('--color', '109, 62, 103');
            break;
        case 'staging':
            r.style.setProperty('--color', '96, 54, 170');
            break;
        case 'production':
            r.style.setProperty('--color', '45, 126, 214');
            break;
        case 'demo':
            r.style.setProperty('--color', '193, 142, 60');
            break;
        case 'demo2':
            r.style.setProperty('--color', '193, 142, 60');
            break;
        case 'demo3':
            r.style.setProperty('--color', '193, 142, 60');
            break;
        case 'opsdemo':
            r.style.setProperty('--color', '139, 9, 45');
            break;
        case 'training':
            r.style.setProperty('--color', '0, 122, 91');
            break;
        case 'uat':
            r.style.setProperty('--color', '137, 137, 137');
            break;
        case 'dev':
            r.style.setProperty('--color', '181, 43, 40');
            break;
        case 'archive':
            r.style.setProperty('--color', '49, 49, 52');
            break;
        case 'preprod':
            r.style.setProperty('--color', '49, 49, 52');
            break;
        case 'devtraining':
            r.style.setProperty('--color', '181, 43, 40');
            break;
        case 'workingtraining':
            r.style.setProperty('--color', '0, 122, 91');
            break;
        case 'beta':
            r.style.setProperty('--color', '129, 34, 0');
            break;
        default:
            r.style.setProperty('--color', '45, 126, 214');
            break;
    }
});
